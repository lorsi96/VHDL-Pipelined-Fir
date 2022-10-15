from typing import Callable, Iterable, List
import cocotb
import numpy as np
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from utils import (
    load_float_coeffs_from_data,
    fxp_binary_value_to_float,
    float_to_fixed,
    S1616_MIN,
    S1616_MAX,
)
from duts import Clockable, Filter

TEST_DURATION_NS = 100

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
    await RisingEdge(dut.clk_i)  # Don't capture unil fist compute completes.
    while True:
        await FallingEdge(dut.clk_i)
        arr.append(fxp_binary_value_to_float(dut.data_o))


# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #
async def __test_filter_single_output(
    dut: Filter, data_in: float, coeffs: Iterable[float], exp_val: float
):
    dut.clk_i.value = 0
    dut.reset_i.value = 0
    dut.data_i.value = float_to_fixed(data_in)

    for signal, coef in zip(dut.coeffs_i, coeffs):
        signal.value = float_to_fixed(coef)

    # Reset Pulse
    dut.reset_i.value = 1
    await Timer(10, units="ns")
    dut.reset_i.value = 0
    await Timer(10, units="ns")

    # Test
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o, dtype="S16.16")
    assert res == exp_val, f"Incorrect result {res}"


@cocotb.test()
async def single_coef_test(dut: Filter):
    test_coeffs = np.zeros(len(dut.coeffs_i))
    test_coeffs[0] = 2.0
    din = 2.0
    exp = 4.0

    await __test_filter_single_output(dut, din, test_coeffs, exp)


@cocotb.test()
async def positive_saturation_test(dut: Filter):
    test_coeffs = np.ones(len(dut.coeffs_i))
    din = S1616_MAX
    exp = S1616_MAX

    await __test_filter_single_output(dut, din, test_coeffs, exp)


@cocotb.test()
async def negative_saturation_test(dut: Filter):
    test_coeffs = np.ones(len(dut.coeffs_i))
    din = S1616_MIN
    exp = S1616_MIN

    await __test_filter_single_output(dut, din, test_coeffs, exp)


@cocotb.test()
async def positive_saturation_neg_operands_test(dut: Filter):
    test_coeffs = -np.ones(len(dut.coeffs_i))
    din = S1616_MIN
    exp = S1616_MAX

    await __test_filter_single_output(dut, din, test_coeffs, exp)
