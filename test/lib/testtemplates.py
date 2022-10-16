import numpy as np
import lib.duts as duts
import cocotb
from cocotb.triggers import Timer
from typing import Iterable, List, Sequence, Optional
import os
import lib.conversions as conversions
import lib.cocoutils as cocoutils


async def test_steady_state_filter_output_with_constant_input(
    dut: duts.Filter,
    data_in: float,
    coeffs: Iterable[float],
    exp_val: float,
    out_dtype: str = "S16.16",
):
    """
    Given a DUT with a filter-like interface, it configures its coefficients,
    sends a single value through it until the output stablishes and compares
    it to an expected value.

    Args:
        dut (Filter)
        data_in (float): value to be fixed at the filter's input.
        coeffs (Iterable[float]): filter coefficients.
        exp_val (float): expected value at output.
    """
    dut.clk_i.value = 0
    dut.reset_i.value = 0
    dut.data_i.value = conversions.float_to_fixed(data_in)

    for signal, coef in zip(dut.coeffs_i, coeffs):
        signal.value = conversions.float_to_fixed(coef)

    # Generate reset signal
    await cocoutils.reset_dut(dut)

    # Test
    await cocotb.start(cocoutils.generate_clock(dut))
    await Timer(100, units="ns")  # type: ignore
    res = conversions.fxp_binary_value_to_float(dut.data_o, dtype=out_dtype)
    assert res == exp_val, f"Incorrect result {res}"


async def test_real_filter_template(
    dut: duts.Filter,
    input_signal: Sequence[float],
    coeffs: Sequence[float],
    output_dtype: str = "S91.32",
    max_error_tolerance: float = 2**15,
    test_duration_ns: int = 100,
    output_data_dir: Optional[str] = None,
):
    """
    Given a DUT with a filter-like interface, it passes the input signal
    through the filter and compares the output sample-to-sample with a python
    computed filter with the same coefficients.

    Note that, given the filter architecture, first two output samples will
    always be 0, so comparison starts from the third output sample onwards.

    Also note that this test template DOES NOT LOAD THE COEFFICIENTS ONTO
    THE DUT, it has to be done before calling this function.

    Args:
        dut (duts.Filter):
        input_signal (Sequence[float]): signal to be passed throught the filter.
        coeffs (Sequence[float]): coefficients, only used to compute the filter
            output using numpy. DOESNT LOAD THE COEFFS TO THE DUT.
        output_dtype (str, optional): DUT's ouput type. Defaults to "S91.32".
        max_error_tolerance (float, optional): Max permitted difference between
            dut's output samples and python-computed output. Defaults to 2**15.
        test_duration_ns (int, optional): Defaults to 100 ns.
        output_data_dir (Optional[str], optional): if set, will save the output
            of both the dut's filter samples and python's output. Defaults to
            None.
    """
    # Capture output container
    output: List[float] = list()

    # Reset pulse.
    await cocoutils.reset_dut(dut)

    # Let the simulation begin.
    await cocotb.start(cocoutils.generate_clock(dut))
    await cocotb.start(cocoutils.feed_samples(dut, input_signal))
    await cocotb.start(cocoutils.capture_output(dut, output, dtype=output_dtype))
    await Timer(test_duration_ns, units="ns")  # type: ignore

    # Compute expected output.
    arch_delay = np.zeros(2)
    filtered = np.convolve(input_signal, coeffs, mode="full")
    compare = np.concatenate([arch_delay, filtered])
    compare = np.trim_zeros(compare, "b")  # Remove trailling zeroes.

    # Getting DUT output.
    output_ndarray = np.array(output)

    # Saving output for further analysis.
    if output_data_dir is not None:
        abs_path = lambda f: str(os.path.join(output_data_dir, f))
        np.save(abs_path("dut_data"), output_ndarray, allow_pickle=True)
        np.save(abs_path("python_data"), compare, allow_pickle=True)

    # Assertions.
    for expected, actual in zip(compare, output_ndarray):
        assert (
            np.abs(expected - actual) < max_error_tolerance
        ), f"{expected} VS {actual}"
