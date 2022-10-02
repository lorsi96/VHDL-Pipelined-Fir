library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

package fir_pkg is
    constant FIR_COEFFICIENT_WIDTH : integer := 32;
    constant FIR_DATA_WIDTH        : integer := 32;
    constant FIR_MAX_TAPS_N        : integer := 60;

    constant FIR_MAC_WIDTH         : integer := FIR_COEFFICIENT_WIDTH + FIR_DATA_WIDTH;
    constant FIR_FILTER_OUT_WIDTH  : integer := FIR_MAX_TAPS_N + FIR_MAC_WIDTH - 1;

    type fir_coefficients is array(0 to FIR_MAX_TAPS_N-1) of signed(FIR_DATA_WIDTH downto 0);

    -- Coefficients File Loading --

end package;
