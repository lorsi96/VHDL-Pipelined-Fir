import cocotb
from cocotb.triggers import FallingEdge, Timer
from utils import fxp_binary_value_to_float, float_to_fixed
from duts import Clockable, Filter

TEST_DURATION_NS = 1000

# *************************************************************************** #
#                             Testbench Utilities                             #
# *************************************************************************** #
async def generate_clock(dut:Clockable):
    while True: 
        dut.clk_i.value = 0
        await Timer(1, units="ns")
        dut.clk_i.value = 1
        await Timer(1, units="ns")

# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #

@cocotb.test()
async def single_coef_test(dut:Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0
    dut.data_i.value = float_to_fixed(2.0, dtype='S16.16')
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    await FallingEdge(dut.clk_i)
    res = fxp_binary_value_to_float(dut.data_o, dtype='S91.32')
    assert res == 4.0, f"Incorrect result {res}"
