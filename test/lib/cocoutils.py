import lib.duts as duts
import lib.conversions as conversions
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from typing import Iterable, List


# ************************** Generic DUT Utilities ************************** #


async def generate_single_clock_pulse(dut: duts.Clockable):
    dut.clk_i.value = 0
    await Timer(1, units="ns")  # type: ignore
    dut.clk_i.value = 1
    await Timer(1, units="ns")  # type: ignore


async def generate_clock(dut: duts.Clockable):
    while True:
        dut.clk_i.value = 0
        await Timer(1, units="ns")  # type: ignore
        dut.clk_i.value = 1
        await Timer(1, units="ns")  # type: ignore


async def reset_dut(dut: duts.Resetable):
    dut.reset_i.value = 1
    await Timer(1, units="ns")  # type: ignore
    dut.reset_i.value = 0
    await Timer(1, units="ns")  # type: ignore


# ********************** Filter Specific DUT Utilities ********************** #
async def feed_samples(
    dut: duts.Filter, samples: Iterable[float], dtype: str = "S16.16"
):
    for sample in samples:
        dut.data_i.value = conversions.float_to_fixed(sample, dtype)
        await FallingEdge(dut.clk_i)
    dut.data_i.value = 0


async def capture_output(dut: duts.Filter, arr: List[float], dtype: str = "S16.16"):
    await RisingEdge(dut.clk_i)  # Don't capture unil fist compute completes.
    while True:
        await FallingEdge(dut.clk_i)
        arr.append(conversions.fxp_binary_value_to_float(dut.data_o, dtype))
