import itertools
import numpy as np
import cocotb
from typing import Iterable, List
import cocotb
from cocotb.triggers import FallingEdge, Timer
from utils import fxp_binary_value_to_float, float_to_fixed, load_float_coeffs_from_data
from duts import Clockable, Filter
from cocotb.triggers import FallingEdge, Timer
from utils import fxp_binary_value_to_float, float_to_fixed
from duts import Clockable, Filter

TEST_DURATION_NS = 1000
SAVE_OUTPUT_DATA = False

# *************************************************************************** #
#                             Testbench Utilities                             #
# *************************************************************************** #
async def generate_clock(dut: Clockable):
    while True:
        dut.clk_i.value = 0
        await Timer(1, units="ns")
        dut.clk_i.value = 1
        await Timer(1, units="ns")


async def feed_samples(dut: Filter, samples: Iterable[float]):
    for sample in samples:
        dut.data_i.value = float_to_fixed(sample)
        await FallingEdge(dut.clk_i)
    dut.data_i.value = 0


async def capture_output(dut: Filter, arr: List[float]):
    while True:
        await FallingEdge(dut.clk_i)
        arr.append(fxp_binary_value_to_float(dut.data_o, "S91.32"))


# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #
@cocotb.test()
async def single_coef_test(dut: Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0

    first_item = True
    for s1616 in dut.coeffs_i:
        if first_item:
            s1616.value = float_to_fixed(2.0)
            first_item = False
        else:
            s1616.value = 0

    dut.data_i.value = float_to_fixed(2.0, dtype="S16.16")
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    await FallingEdge(dut.clk_i)
    res = fxp_binary_value_to_float(dut.data_o, dtype="S91.32")
    assert res == 4.0, f"Incorrect result {res}"


@cocotb.test()
async def arbitrary_filter_test(dut: Filter):
    # Prepare test signal.
    f_hz = 10
    fs_hz = 200
    n = 20
    test_signal = np.sin(2 * np.pi * f_hz * np.arange(n) / fs_hz)

    # Get coefficients
    coeffs = load_float_coeffs_from_data()

    # Capture output container
    output: List[float] = list()

    # Load coefficients to DUT.
    for c, signal in zip(coeffs, dut.coeffs_i):
        signal.value = float_to_fixed(c)

    # Reset Pulse
    dut.data_i.value = 0
    dut.reset_i.value = 1
    await Timer(10, units="ns")
    dut.reset_i.value = 0

    # Let the simulation begin.
    await cocotb.start(generate_clock(dut))
    await cocotb.start(feed_samples(dut, test_signal))
    await cocotb.start(capture_output(dut, output))
    await Timer(TEST_DURATION_NS, units="ns")

    # Compute expected output.
    arch_delay = np.zeros(2)
    filtered = np.convolve(test_signal, coeffs, mode="full")
    compare = np.concatenate([arch_delay, filtered])
    compare = np.trim_zeros(compare, "b")  # Remove trailling zeroes.

    # Getting DUT output.
    output_ndarray = np.array(output)

    # Saving output for further analysis.
    if SAVE_OUTPUT_DATA:
        np.save("dut_data", output_ndarray, allow_pickle=True)
        np.save("python_data", compare, allow_pickle=True)

    # Assertions.
    tolerance = 2**-15
    for expected, actual in zip(compare, output_ndarray):
        assert np.abs(expected - actual) < tolerance, f"{expected} VS {actual}"
