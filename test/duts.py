from typing import Protocol
from cocotb.binary import BinaryValue

class Saturator(Protocol):

    @property
    def data_i(self) -> BinaryValue:
        ... 

    @property
    def data_o(self) -> BinaryValue:
        ... 
