library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.fir_pkg.all;

entity fir_saturator is
    generic (
        WIDTH_IN  : integer := FIR_FILTER_OUT_WIDTH;
        WIDTH_OUT : integer := FIR_DATA_WIDTH 
    );
    Port ( 
        clk_i: in std_logic;
        data_i : in std_logic_vector((WIDTH_IN - 1) downto 0);
        data_o : out std_logic_vector((WIDTH_OUT - 1) downto 0)
    );
end fir_saturator;

architecture rtl of fir_saturator is

constant OUT_MAX : std_logic_vector((WIDTH_OUT - 1) downto 0) := '0' & (WIDTH_OUT - 2 downto 0 => '1');
constant OUT_MIN : std_logic_vector((WIDTH_OUT - 1) downto 0) := '1' & (WIDTH_OUT - 2 downto 0 => '0');
constant SATURATION_THRESHOLD_HIGH: signed((WIDTH_IN - 1) downto 0) := resize(signed(OUT_MAX), WIDTH_IN - (WIDTH_OUT / 2)) & "1111111111111111";  
constant SATURATION_THRESHOLD_LOW: signed((WIDTH_IN - 1) downto 0) := resize(signed(OUT_MIN), WIDTH_IN - (WIDTH_OUT / 2)) & "0000000000000000";  

begin
    process(clk_i)
    begin
        if rising_edge(clk_i) then
            if signed(data_i) > SATURATION_THRESHOLD_HIGH then
                data_o <= OUT_MAX;
            elsif signed(data_i) < SATURATION_THRESHOLD_LOW then
                data_o <= OUT_MIN;
            else
                data_o <= data_i((WIDTH_OUT + (WIDTH_OUT / 2) - 1) downto (WIDTH_OUT / 2));
            end if;
        end if;
    end process;
end rtl;
