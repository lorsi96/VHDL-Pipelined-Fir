from typing import Protocol
from cocotb.binary import BinaryValue
from cocotb.handle import NonHierarchyIndexableObject


class Clockable(Protocol):
    @property
    def clk_i(self) -> BinaryValue:
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
    def coeffs_i(self) -> NonHierarchyIndexableObject:
        ...

    @property
    def data_o(self) -> BinaryValue:
        ...
