----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 29.09.2022 12:40:20
-- Design Name: 
-- Module Name: saturacion - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity principal is
   Generic 
    (
        COEFF_WIDTH : integer := 8;
        FILTER_TAPS : integer := 8;
        DATA_WIDTH  : integer := 8 
    );
    Port 
    ( 
        clk_i, reset_i :  in STD_LOGIC;
        data_i         :  in STD_LOGIC_VECTOR (DATA_WIDTH - 1 downto 0);
        data_o         : out STD_LOGIC_VECTOR ((COEFF_WIDTH + FILTER_TAPS + DATA_WIDTH - 1) downto 0)
    );
end principal;

architecture Behavioral of principal is

signal data : STD_LOGIC_VECTOR((COEFF_WIDTH + FILTER_TAPS + DATA_WIDTH - 1) downto 0);

begin

    FF: entity work.FIR_Filter generic map 
    (   
        COEFF_WIDTH => COEFF_WIDTH,
        FILTER_TAPS => FILTER_TAPS,
        DATA_WIDTH  => DATA_WIDTH
    )
    port map 
    ( 
        clk_i   =>   clk_i, 
        reset_i => reset_i,
        data_i  =>  data_i,
        data_o  =>  data
    );
    
    SAT: entity work.saturacion generic map
    (   
        WIDTH_IN  => COEFF_WIDTH + FILTER_TAPS + DATA_WIDTH,
        WIDTH_OUT => COEFF_WIDTH + FILTER_TAPS + DATA_WIDTH
    )
    port map 
    (    
        data_i =>   data,
        data_o => data_o
    );
    
end Behavioral;