import fxpmath
from cocotb.binary import BinaryValue
from typing import List, cast

import lib.constants as constants


def float_to_fixed(val: float, dtype="S16.16") -> int:
    fxp = cast(str, fxpmath.Fxp(val, dtype=dtype).bin())
    return int(fxp, base=2)


def fxp_binary_value_to_float(v: BinaryValue, dtype="S16.16") -> float:
    fxp = fxpmath.Fxp(dtype=dtype)
    fxp.set_val("0b" + str(v.value), raw=True)
    return cast(float, fxp.astype(float))


def load_float_coeffs_from_data(file: str = constants.DEFAULT_COEF_FILE) -> List[float]:
    with open(file, "rt") as f:
        return [
            cast(float, fxpmath.Fxp("0b" + l.strip(), dtype="S16.16").astype(float))
            for l in f.readlines()
        ]
