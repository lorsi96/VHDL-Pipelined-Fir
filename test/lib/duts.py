from typing import Protocol, Sequence
from cocotb.binary import BinaryValue


class Clockable(Protocol):
    @property
    def clk_i(self) -> BinaryValue:
        ...


class Resetable(Protocol):
    @property
    def reset_i(self) -> BinaryValue:
        ...


class Saturator(Protocol):
    @property
    def clk_i(self) -> BinaryValue:
        ...

    @property
    def data_i(self) -> BinaryValue:
        ...

    @property
    def data_o(self) -> BinaryValue:
        ...


class Filter(Protocol):
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
    def data_i(self) -> BinaryValue:
        ...

    @property
    def coeffs_i(self) -> Sequence[BinaryValue]:
        ...

    @property
    def data_o(self) -> BinaryValue:
        ...
