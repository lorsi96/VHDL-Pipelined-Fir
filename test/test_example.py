import cocotb
import fxpmath
from typing import cast, Protocol
from cocotb.triggers import FallingEdge, Timer
from cocotb.binary import BinaryValue
# *************************************************************************** #
#                                  DUT Model                                  #
# *************************************************************************** #
class DUT(Protocol):

    @property
    def clk_i(self) -> BinaryValue:
        ... 

    @property
    def reset_i(self) -> BinaryValue:
        ... 

    @property
    def enable_i(self) -> BinaryValue:
        ... 

    @property
    def coefs_i(self) -> BinaryValue:
        ...

    @property
    def data_i(self) -> BinaryValue:
        ... 

    @property
    def data_o(self) -> BinaryValue:
        ... 


# *************************************************************************** #
#                            Fixed Point Utilities                            #
# *************************************************************************** #
def float_to_s1616(val:float) -> int:
    fxp = cast(str, fxpmath.Fxp(val, dtype='S16.16').bin()) 
    return int(fxp, base=2)

def fixed_to_float(val:int, dtype:str='S16.16') -> float:
    try:
        empty = fxpmath.Fxp(dtype=dtype)
        empty.set_val(int(val), raw=True)
        return float(empty.astype(float))  # type: ignore
    except ValueError:
        return float('inf')

def s1616_to_float(val:int) -> float:
    return fixed_to_float(val, dtype='S16.16')

def s3232_to_float(val:int) -> float:
    return fixed_to_float(val, dtype='S32.32')


# *************************************************************************** #
#                             Testbench Utilities                             #
# *************************************************************************** #
async def generate_clock(dut:DUT):
    while True: 
        dut.clk_i.value = 0
        await Timer(1, units="ns")
        dut.clk_i.value = 1
        await Timer(1, units="ns")

# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #
TEST_DURATION_NS = 20


@cocotb.test()
async def my_second_test(dut:DUT):
    dut.clk_i.value = 0
    dut.data_i.value = float_to_s1616(2.0)
    dut.coefs_i.value = float_to_s1616(1.0)

    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    await FallingEdge(dut.clk_i)

    res = s1616_to_float(dut.data_o.value)
    assert res == 2.0, f"Incorrect result {res}"