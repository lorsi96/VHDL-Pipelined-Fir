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
           coefs_i  : in STD_LOGIC_VECTOR (FILTER_TAPS-1 downto 0);
           data_i   : in STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0);
           data_o   : out STD_LOGIC_VECTOR (DATA_WIDTH-1 downto 0) := (others => '0')
    );
end parallel_fir_filter;
 
architecture parallel_fir_filter_arch of parallel_fir_filter is
begin 

-- Combinational --
    data_o <= data_i;

-- Procedural -- 
process(clk_i)
begin
    if rising_edge(clk_i) then
        -- Procedural Logic --
    end if;
end process;
end parallel_fir_filter_arch;