library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
use std.textio.all;

library work;
use work.fir_pkg.all;

entity fir_filter is
    generic (
        COEFF_WIDTH : integer := FIR_COEFFICIENT_WIDTH;
        FILTER_TAPS : integer := FIR_MAX_TAPS_N;
        DATA_WIDTH  : integer := FIR_DATA_WIDTH
    );
    port ( 
        clk_i, reset_i :  in std_logic;
        coeffs_i       :  in fir_coefficients;
        data_i         :  in std_logic_vector (DATA_WIDTH - 1 downto 0);
        data_o         : out std_logic_vector (FIR_FILTER_OUT_WIDTH - 1 downto 0)
    );
end fir_filter;

architecture rtl of fir_filter is

-- Use DSP Cells for synthesis --
attribute use_dsp : string;
attribute use_dsp of rtl : architecture is "yes";

-- Registers --
type input_registers is array(0 to FILTER_TAPS - 1) of signed(DATA_WIDTH - 1 downto 0);
signal areg_s  : input_registers := (others=>(others=>'0'));

type mult_registers is array(0 to FILTER_TAPS - 1) of signed((COEFF_WIDTH + DATA_WIDTH - 1) downto 0);
signal mreg_s : mult_registers := (others=>(others=>'0'));

type dsp_registers is array(0 to FILTER_TAPS) of signed( (FIR_FILTER_OUT_WIDTH - 1) downto 0);
signal preg_s : dsp_registers := (others=>(others=>'0'));

-- rtl --
begin  
    data_o <= std_logic_vector(preg_s(0));         
    process(clk_i, reset_i)
    begin
        if reset_i='1' then
            for i in 0 to FILTER_TAPS-1 loop
                areg_s(i) <=(others=> '0');
                mreg_s(i) <=(others=> '0');
                preg_s(i) <=(others=> '0');
            end loop;
        elsif rising_edge(clk_i) then
            for i in 0 to FILTER_TAPS-1 loop
                areg_s(i) <= signed(data_i);
                mreg_s(i) <= areg_s(i) * coeffs_i(i);         
                preg_s(i) <= mreg_s(i) + preg_s(i+1);
            end loop; 
        end if;
    end process;
end rtl;
