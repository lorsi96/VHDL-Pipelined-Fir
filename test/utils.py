import fxpmath
from cocotb.binary import BinaryValue
from typing import cast 


def float_to_fixed(val:float, dtype='S16.16') -> int:
    fxp = cast(str, fxpmath.Fxp(val, dtype=dtype).bin()) 
    return int(fxp, base=2)

def fxp_binary_value_to_float(v: BinaryValue, dtype='S16.16') -> float:
    fxp = fxpmath.Fxp(dtype=dtype)
    fxp.set_val('0b' + str(v.value), raw=True)
    return cast(float, fxp.astype(float))
