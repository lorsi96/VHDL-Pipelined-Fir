import cocotb
from cocotb.triggers import Timer

from utils import float_to_fixed, fxp_binary_value_to_float
from duts import Saturator

TEST_DURATION_NS = 1000

S1616_MAX = 2**15 - 2**-16
S1616_MIN = -(2**15)

# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #

@cocotb.test()
async def no_saturation(dut:Saturator):
    test_val = 4.
    dut.data_i.value = float_to_fixed(test_val, dtype='S91.32')
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o)
    print(dut.data_i.value)
    print(dut.data_o.value)
    assert test_val == res, f"Out value was {res} VS {test_val}"

@cocotb.test()
async def dont_saturate_positive(dut:Saturator):
    dut.data_i.value = float_to_fixed(S1616_MAX, dtype='S91.32')
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o)
    print(dut.data_i.value)
    print(dut.data_o.value)
    assert S1616_MAX == res, f"Out value was {res} VS {S1616_MAX}"

@cocotb.test()
async def dont_saturate_negative(dut:Saturator):
    dut.data_i.value = float_to_fixed(S1616_MIN, dtype='S91.32')
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o)
    print(dut.data_i.value)
    print(dut.data_o.value)
    assert (S1616_MIN) == res, f"Out value was {res} VS {S1616_MIN}"

@cocotb.test()
async def saturate_upper(dut:Saturator):
    dut.data_i.value = float_to_fixed(S1616_MAX + 1, dtype='S91.32')
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o)
    print(dut.data_i.value)
    print(dut.data_o.value)
    assert S1616_MAX == res, f"Out value was {res} VS {S1616_MAX}"

@cocotb.test()
async def saturate_lower(dut:Saturator):
    dut.data_i.value = float_to_fixed(S1616_MIN - 1, dtype='S91.32')
    await Timer(TEST_DURATION_NS, units="ns")
    res = fxp_binary_value_to_float(dut.data_o)
    print(dut.data_i.value)
    print(dut.data_o.value)
    assert S1616_MIN == res, f"Out value was {res} VS {S1616_MIN}"
