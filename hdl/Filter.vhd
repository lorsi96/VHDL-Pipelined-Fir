----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 26.09.2022 18:36:55
-- Design Name: 
-- Module Name: Filter - Behavioral
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
use STD.TEXTIO.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity FIR_Filter is
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
end FIR_Filter;

architecture Behavioral of FIR_Filter is

attribute use_dsp : string;
attribute use_dsp of Behavioral : architecture is "yes";

constant  MAC_WIDTH : integer := COEFF_WIDTH + DATA_WIDTH + FILTER_TAPS;

type input_registers is array(0 to FILTER_TAPS - 1) of signed(DATA_WIDTH - 1 downto 0);
signal areg_s  : input_registers := (others=>(others=>'0'));

-- type coeff_registers is array(0 to FILTER_TAPS-1) of signed( (MAC_WIDTH-1) downto 0);
-- signal breg_s : coeff_registers := (others=>(others=>'0'));

type mult_registers is array(0 to FILTER_TAPS - 1) of signed( (COEFF_WIDTH + DATA_WIDTH - 1) downto 0);
signal mreg_s : mult_registers := (others=>(others=>'0'));

type dsp_registers is array(0 to FILTER_TAPS) of signed( (MAC_WIDTH - 1) downto 0);
signal preg_s : dsp_registers := (others=>(others=>'0'));

subtype coe_data is bit_vector ((COEFF_WIDTH - 1) downto 0);
type DATA_TYPE is array (0 to (FILTER_TAPS - 1)) of coe_data;

impure function initFromFile (DataFileName : in string) return DATA_TYPE is

File     DataFile        : text is in DataFileName;
variable DataFileLine    : line;
variable DATA            : DATA_TYPE;

begin
    for i in DATA_TYPE'range loop    
        readline(DataFile,DataFileLine);
        read(DataFileLine, DATA(i));
    end loop;
   return DATA;
end function;

signal coeff_data : DATA_TYPE := initFromFile("C:\Users\josed\OneDrive - UNIVERSIDAD DE CUNDINAMARCA\Programacion\Vivado\2022\DPS_MSE\data_file_init.data");

begin  

-- Coefficient formatting
-- Coeff_Array: for i in 0 to FILTER_TAPS-1 generate
--               breg_s(i) <= signed(to_stdlogicvector(coeff_data(i)));
-- end generate;

data_o <= std_logic_vector(preg_s(0)( MAC_WIDTH-1 downto 0));         
      
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
                    mreg_s(i) <= areg_s(i) * signed(to_stdlogicvector(coeff_data(i)));         
                    -- mreg_s(i) <= areg_s(i) * breg_s(i);         
                    preg_s(i) <= mreg_s(i) + preg_s(i+1);
                    
                end loop; 
            end if;            
        
        end if;
        
    end process;
    
end Behavioral;
