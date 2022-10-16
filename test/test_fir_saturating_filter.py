import cocotb
import numpy as np

from lib import duts, constants, testtemplates

TEST_DURATION_NS = 100

# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #


@cocotb.test()  # type: ignore
async def single_coef_test(dut: duts.Filter):
    test_coeffs = np.zeros(len(dut.coeffs_i))
    test_coeffs[0] = 2.0
    din = 2.0
    exp = 4.0

    await testtemplates.test_steady_state_filter_output_with_constant_input(
        dut, din, test_coeffs, exp
    )


@cocotb.test()  # type: ignore
async def positive_saturation_test(dut: duts.Filter):
    test_coeffs = np.ones(len(dut.coeffs_i))
    din = constants.S1616_MAX
    exp = constants.S1616_MAX

    await testtemplates.test_steady_state_filter_output_with_constant_input(
        dut, din, test_coeffs, exp
    )


@cocotb.test()  # type: ignore
async def negative_saturation_test(dut: duts.Filter):
    test_coeffs = np.ones(len(dut.coeffs_i))
    din = constants.S1616_MIN
    exp = constants.S1616_MIN

    await testtemplates.test_steady_state_filter_output_with_constant_input(
        dut, din, test_coeffs, exp
    )


@cocotb.test()  # type: ignore
async def positive_saturation_neg_operands_test(dut: duts.Filter):
    test_coeffs = -np.ones(len(dut.coeffs_i))
    din = constants.S1616_MIN
    exp = constants.S1616_MAX

    await testtemplates.test_steady_state_filter_output_with_constant_input(
        dut, din, test_coeffs, exp
    )
