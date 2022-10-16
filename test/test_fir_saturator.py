import cocotb
from cocotb.triggers import Timer

from lib import duts, conversions, constants, cocoutils

TEST_DURATION_NS = 1000

# *************************************************************************** #
#                               Tests Templates                               #
# *************************************************************************** #
async def __test_saturator_output(dut: duts.Saturator, din: float, dout: float):
    dut.data_i.value = conversions.float_to_fixed(din, dtype="S91.32")
    await cocoutils.generate_single_clock_pulse(dut)
    await Timer(TEST_DURATION_NS, units="ns")  # type: ignore
    res = conversions.fxp_binary_value_to_float(dut.data_o)
    assert dout == res, f"Out value was {res} VS {din}"


# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #


@cocotb.test()  # type: ignore
async def no_saturation(dut: duts.Saturator):
    await __test_saturator_output(dut, 4.0, 4.0)


@cocotb.test()  # type: ignore
async def dont_saturate_positive(dut: duts.Saturator):
    await __test_saturator_output(dut, constants.S1616_MAX, constants.S1616_MAX)


@cocotb.test()  # type: ignore
async def dont_saturate_negative(dut: duts.Saturator):
    await __test_saturator_output(dut, constants.S1616_MIN, constants.S1616_MIN)


@cocotb.test()  # type: ignore
async def saturate_upper(dut: duts.Saturator):
    await __test_saturator_output(dut, constants.S1616_MAX + 1, constants.S1616_MAX)


@cocotb.test()  # type: ignore
async def saturate_lower(dut: duts.Saturator):
    await __test_saturator_output(dut, constants.S1616_MIN - 1, constants.S1616_MIN)
