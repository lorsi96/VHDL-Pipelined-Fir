import cocotb
import numpy as np
from lib import duts, conversions, testtemplates

TEST_DURATION_NS = 100
SAVE_FILTER_OUTPUT = True

# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #
@cocotb.test()  # type: ignore
async def real_filter_test(dut: duts.Filter):
    # Prepare test signal.
    f_hz = 10
    fs_hz = 200
    n = 20
    test_signal = np.sin(2 * np.pi * f_hz * np.arange(n) / fs_hz)

    # Load coefficients.
    coeffs = conversions.load_float_coeffs_from_data()

    # Run test.
    await testtemplates.test_real_filter_template(
        dut, test_signal, coeffs, "S32.32"  # type: ignore
    )
