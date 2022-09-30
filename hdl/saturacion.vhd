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

entity saturacion is
    generic
    (
        WIDTH_IN  : integer := 8;
        WIDTH_OUT : integer := 8 
    );
    Port 
    ( 
        data_i :  in std_logic_vector( ( WIDTH_IN - 1) downto 0);
        data_o : out std_logic_vector( (WIDTH_OUT - 1) downto 0)
    );
end saturacion;

architecture Behavioral of saturacion is

constant max : bit_vector((WIDTH_OUT - 1) downto 0) := ((WIDTH_OUT - 1) => '0', others=>'1');
constant min : bit_vector((WIDTH_OUT - 1) downto 0) := ((WIDTH_OUT - 1) => '1', others=>'0');

signal data : signed((WIDTH_IN - 1) downto 0);

begin

    process(data_i, data)
    
    begin
    
        data <= signed(data_i);
    
        if data > (2**(WIDTH_OUT-1))-1 then
            data_o <= to_stdlogicvector(max);
        elsif data < -(2**WIDTH_OUT) then
            data_o <= to_stdlogicvector(min);
        else
            data_o <= std_logic_vector(data);
        end if;

    end process;
    
end Behavioral;
