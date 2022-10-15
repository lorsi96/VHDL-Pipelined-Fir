import itertools
import cocotb
from typing import Iterable, List
import cocotb
from cocotb.triggers import FallingEdge, Timer
from utils import (
    fxp_binary_value_to_float,
    float_to_fixed,
)
from duts import Clockable, Filter
from cocotb.triggers import FallingEdge, Timer
from utils import fxp_binary_value_to_float, float_to_fixed
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
        arr.append(fxp_binary_value_to_float(dut.data_o, "S91.32"))


# *************************************************************************** #
#                                    Tests                                    #
# *************************************************************************** #
@cocotb.test()
async def single_coef_test(dut: Filter):
    dut.clk_i.value = 0
    dut.reset_i = 0

    first_item = True
    for s1616, index in zip(dut.coeffs_i, range(60)):
        print(f"Iterating {index}")
        if first_item:
            s1616.value = float_to_fixed(2.0)
            first_item = False
        else:
            s1616.value = 0

    dut.data_i.value = float_to_fixed(2.0, dtype="S16.16")
    await cocotb.start(generate_clock(dut))
    await Timer(TEST_DURATION_NS, units="ns")
    await FallingEdge(dut.clk_i)
    res = fxp_binary_value_to_float(dut.data_o, dtype="S91.32")
    assert res == 4.0, f"Incorrect result {res}"
