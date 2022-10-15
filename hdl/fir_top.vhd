library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.fir_pkg.all;

entity fir_top is
   Generic (DATA_WIDTH  : integer := FIR_DATA_WIDTH);
    Port ( 
        clk_i, reset_i :  in std_logic;
        data_i         :  in std_logic_vector (DATA_WIDTH - 1 downto 0);
        data_o         : out std_logic_vector (DATA_WIDTH - 1 downto 0)
    );
end fir_top;


architecture rtl of fir_top is

signal coeffs: fir_coefficients;

begin

    fir_coef_loader: entity work.fir_coef_loader
    port map ( 
        coeffs_out => coeffs 
    );
    
    fir_saturating_filter_inst: entity work.fir_saturating_filter 
    port map ( 
        clk_i    =>   clk_i, 
        coeffs_i => coeffs,
        reset_i  =>  reset_i,
        data_i   =>  data_i,
        data_o   =>  data_o
    );

end rtl;
