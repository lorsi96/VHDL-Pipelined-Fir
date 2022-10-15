import fxpmath
import duts
from cocotb.binary import BinaryValue
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from typing import Iterable, List, cast
import os


S1616_MAX = 2**15 - 2**-16
S1616_MIN = -(2**15)
BASE_NAME = "../data/data_file_init.data"
DEFAULT_COEF_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), BASE_NAME)

# *************************************************************************** #
#                          Float <-> Fixed Utilities                          #
# *************************************************************************** #
def float_to_fixed(val: float, dtype="S16.16") -> int:
    fxp = cast(str, fxpmath.Fxp(val, dtype=dtype).bin())
    return int(fxp, base=2)


def fxp_binary_value_to_float(v: BinaryValue, dtype="S16.16") -> float:
    fxp = fxpmath.Fxp(dtype=dtype)
    fxp.set_val("0b" + str(v.value), raw=True)
    return cast(float, fxp.astype(float))


def load_float_coeffs_from_data(file: str = DEFAULT_COEF_FILE) -> List[float]:
    with open(file, "rt") as f:
        return [
            cast(float, fxpmath.Fxp("0b" + l.strip(), dtype="S16.16").astype(float))
            for l in f.readlines()
        ]


# *************************************************************************** #
#                               CocoTb Utilities                              #
# *************************************************************************** #

# ************************** Generic DUT Utilities ************************** #
async def generate_clock(dut: duts.Clockable):
    while True:
        dut.clk_i.value = 0
        await Timer(1, units="ns")
        dut.clk_i.value = 1
        await Timer(1, units="ns")


async def reset_dut(dut: duts.Resetable):
    dut.reset_i.value = 1
    await Timer(1, units="ns")
    dut.reset_i.value = 0
    await Timer(1, units="ns")


# ********************** Filter Specific DUT Utilities ********************** #
async def feed_samples(
    dut: duts.Filter, samples: Iterable[float], dtype: str = "S16.16"
):
    for sample in samples:
        dut.data_i.value = float_to_fixed(sample, dtype)
        await FallingEdge(dut.clk_i)
    dut.data_i.value = 0


async def capture_output(dut: duts.Filter, arr: List[float], dtype: str = "S16.16"):
    await RisingEdge(dut.clk_i)  # Don't capture unil fist compute completes.
    while True:
        await FallingEdge(dut.clk_i)
        arr.append(fxp_binary_value_to_float(dut.data_o, dtype))


# *************************************************************************** #
#                                Test Templates                               #
# *************************************************************************** #
