import numpy as np
import cocotb
import cocotb
from lib import duts, conversions, testtemplates

TEST_DURATION_NS = 1000
SAVE_OUTPUT_DATA = False

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
        dut, din, test_coeffs, exp, out_dtype="S91.32"
    )


@cocotb.test()  # type: ignore
async def real_filter_test(dut: duts.Filter):
    # Prepare test signal.
    f_hz = 10
    fs_hz = 200
    n = 20
    test_signal = np.sin(2 * np.pi * f_hz * np.arange(n) / fs_hz)

    # Get coefficients from file, like the top module does.
    coeffs = conversions.load_float_coeffs_from_data()

    # Load coefficients to DUT.
    for c, signal in zip(coeffs, dut.coeffs_i):
        signal.value = conversions.float_to_fixed(c)

    # Run Test.
    await testtemplates.test_real_filter_template(
        dut, test_signal, coeffs, "S91.32"  # type: ignore
    )
