import numpy as np
import cocotb
from typing import List
import cocotb
from cocotb.triggers import FallingEdge, Timer
from duts import Filter
import utils

TEST_DURATION_NS = 1000
SAVE_OUTPUT_DATA = False

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
            s1616.value = utils.float_to_fixed(2.0)
            first_item = False
        else:
            s1616.value = 0

    dut.data_i.value = utils.float_to_fixed(2.0, dtype="S16.16")
    await cocotb.start(utils.generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    await FallingEdge(dut.clk_i)
    res = utils.fxp_binary_value_to_float(dut.data_o, dtype="S91.32")
    assert res == 4.0, f"Incorrect result {res}"


@cocotb.test()
async def arbitrary_filter_test(dut: Filter):
    # Prepare test signal.
    f_hz = 10
    fs_hz = 200
    n = 20
    test_signal = np.sin(2 * np.pi * f_hz * np.arange(n) / fs_hz)

    # Get coefficients
    coeffs = utils.load_float_coeffs_from_data()

    # Capture output container
    output: List[float] = list()

    # Load coefficients to DUT.
    for c, signal in zip(coeffs, dut.coeffs_i):
        signal.value = utils.float_to_fixed(c)

    # Reset Pulse
    dut.data_i.value = 0
    dut.reset_i.value = 1
    await Timer(10, units="ns")
    dut.reset_i.value = 0

    # Let the simulation begin.
    await cocotb.start(utils.generate_clock(dut))
    await cocotb.start(utils.feed_samples(dut, test_signal))
    await cocotb.start(utils.capture_output(dut, output, "S91.32"))
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
