library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

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

signal data : signed((WIDTH_OUT - 1) downto 0);

begin

    process(data_i)
    
    begin
    
        data <= signed(data_i);
    
        if data > (2**(WIDTH_IN-1))-1 then
            data_o <= to_stdlogicvector(max);
        elsif data < -(2**WIDTH_IN) then
            data_o <= to_stdlogicvector(min);
        else
            data_o <= std_logic_vector(data);
        end if;

    end process;
    
end Behavioral;
