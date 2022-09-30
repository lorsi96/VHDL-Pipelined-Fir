library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

package pds_fir_package is
    type fir_coefficients is array(59 downto 0) of signed(31 downto 0);
end package;

use work.pds_fir_package.all;
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity parallel_fir_filter is
    Generic (
        FILTER_TAPS  : integer := 60;
        DATA_WIDTH  : integer := 32
    ); 
    Port ( 
           clk_i    : in STD_LOGIC;
           reset_i  : in STD_LOGIC;
           enable_i : in STD_LOGIC;
           coefs_i  : in fir_coefficients;
           data_i   : in STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0);
           data_o   : out STD_LOGIC_VECTOR(DATA_WIDTH-1 downto 0) := (others => '0')
    );
end parallel_fir_filter;
 
architecture parallel_fir_filter_arch of parallel_fir_filter is
 
constant MAC_WIDTH : integer := 2 * DATA_WIDTH;
 
type input_registers is array(0 to FILTER_TAPS-1) of signed(DATA_WIDTH-1 downto 0);
signal areg_s  : input_registers := (others=>(others=>'0'));
 
type mult_registers is array(0 to FILTER_TAPS-1) of signed(2 * DATA_WIDTH-1 downto 0);
signal mreg_s : mult_registers := (others=>(others=>'0'));
 
type dsp_registers is array(0 to FILTER_TAPS-1) of signed(MAC_WIDTH-1 downto 0);
signal preg_s : dsp_registers := (others=>(others=>'0'));
 
signal dout_s : std_logic_vector(MAC_WIDTH-1 downto 0);
signal sign_s : signed(MAC_WIDTH - (2 * DATA_WIDTH) + 1 downto 0) := (others=>'0');
 
begin 
data_o <= std_logic_vector(preg_s(0)(MAC_WIDTH-(DATA_WIDTH/2)-1 downto (DATA_WIDTH/2)));         
       
 
process(clk_i)
begin
 
if rising_edge(clk_i) then
 
    if (reset_i = '1') then
        for i in 0 to FILTER_TAPS-1 loop
            areg_s(i) <=(others=> '0');
            mreg_s(i) <=(others=> '0');
            preg_s(i) <=(others=> '0');
        end loop;
 
    elsif (reset_i = '0') then       
        for i in 0 to FILTER_TAPS-1 loop
            areg_s(i) <= signed(data_i); 
       
            if (i < FILTER_TAPS-1) then
                mreg_s(i) <= areg_s(i) * coefs_i(i);         
                preg_s(i) <= mreg_s(i) + preg_s(i+1);
                         
            elsif (i = FILTER_TAPS-1) then
                mreg_s(i) <= areg_s(i) * coefs_i(i); 
                preg_s(i)<= mreg_s(i);
            end if;
        end loop; 
    end if;
     
end if;
end process;
 
end parallel_fir_filter_arch;
