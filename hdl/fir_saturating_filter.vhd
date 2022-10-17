library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.fir_pkg.all;

entity fir_saturating_filter is
   Generic (
        COEFF_WIDTH : integer := FIR_COEFFICIENT_WIDTH;
        FILTER_TAPS : integer := FIR_MAX_TAPS_N;
        DATA_WIDTH  : integer := FIR_DATA_WIDTH 
    );
    Port 
    ( 
        clk_i, reset_i :  in std_logic;
        coeffs_i       :  in fir_coefficients;
        data_i         :  in std_logic_vector (DATA_WIDTH - 1 downto 0);
        data_o         : out std_logic_vector (DATA_WIDTH - 1 downto 0)
    );
end fir_saturating_filter;

architecture rtl of fir_saturating_filter is

signal data : std_logic_vector(FIR_FILTER_OUT_WIDTH - 1 downto 0);

begin
    
    fir_filter_inst: entity work.fir_filter 
    port map ( 
        clk_i    =>   clk_i, 
        coeffs_i =>  coeffs_i,
        reset_i  =>  reset_i,
        data_i   =>  data_i,
        data_o   =>  data
    );

    fir_saturator_inst : entity work.fir_saturator 
    port map (    
        clk_i => clk_i,
        data_i => data,
        data_o => data_o
    );

end rtl;
