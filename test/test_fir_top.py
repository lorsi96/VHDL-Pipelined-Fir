from typing import Callable, Iterable, List
import cocotb
import numpy as np
import pyfda
from cocotb.triggers import FallingEdge, Timer
from utils import (
    load_float_coeffs_from_data,
    fxp_binary_value_to_float,
    float_to_fixed,
    S1616_MIN,
    S1616_MAX,
)
from duts import Clockable, Filter

TEST_DURATION_NS = 1000

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
        arr.append(fxp_binary_value_to_float(dut.data_o))


# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #


@cocotb.test()
async def single_coef_test(dut: Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0
    dut.data_i.value = float_to_fixed(2.0, dtype="S16.16")
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o, dtype="S16.16")
    assert res == 4.0, f"Incorrect result {res}"


@cocotb.test()
async def positive_saturation_test(dut: Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0
    dut.data_i.value = float_to_fixed(S1616_MAX, dtype="S16.16")
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o, dtype="S16.16")
    assert res == S1616_MAX, f"Incorrect result {res}"


@cocotb.test()
async def negative_saturation_test(dut: Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0
    dut.data_i.value = float_to_fixed(S1616_MIN, dtype="S16.16")
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o, dtype="S16.16")
    assert res == S1616_MIN, f"Incorrect result {res}"


@cocotb.test()
async def arbitrary_filter_test(dut: Filter):
    # Prepare test signal.
    f_hz = 10
    fs_hz = 200
    n = 20
    test_signal = np.sin(2 * np.pi * f_hz * np.arange(n) / fs_hz)

    # Capture output container
    output: List[float] = list()

    # Reset Pulse
    dut.reset_i = 1
    await Timer(10, units="ns")
    dut.reset_i = 0

    # Let the simulation begin.
    await cocotb.start(generate_clock(dut))
    await cocotb.start(feed_samples(dut, test_signal))
    await cocotb.start(capture_output(dut, output))
    await Timer(TEST_DURATION_NS, units="ns")

    # Compute expected output.
    coeffs = load_float_coeffs_from_data()
    arch_delay = np.zeros(2)
    filtered = np.convolve(test_signal, coeffs, mode="full")
    compare = np.concatenate([arch_delay, filtered])
    compare = np.trim_zeros(compare, "b")  # Remove trailling zeroes.

    # Assertions.
    output_ndarray = np.array(output)
    tolerance = 0.001
    for expected, actual in zip(compare, output_ndarray):
        # print(f"--{i}--")
        # print(expected)
        # print(actual)
        # print("------")
        assert np.abs(expected - actual) < tolerance
