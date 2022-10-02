library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
use std.textio.all;

library work;
use work.fir_pkg.all;

entity fir_filter is
    Generic 
    (
        COEFF_WIDTH : integer := FIR_COEFFICIENT_WIDTH;
        FILTER_TAPS : integer := FIR_MAX_TAPS_N;
        DATA_WIDTH  : integer := FIR_DATA_WIDTH;
        COEFFS_FILE  : string := "../data/data_file_init.data"
    );
    Port 
    ( 
        clk_i, reset_i :  in std_logic;
        data_i         :  in std_logic_vector (DATA_WIDTH - 1 downto 0);
        data_o         : out std_logic_vector (FIR_FILTER_OUT_WIDTH - 1 downto 0)
    );
end fir_filter;

architecture Behavioral of fir_filter is

attribute use_dsp : string;
attribute use_dsp of Behavioral : architecture is "yes";


type input_registers is array(0 to FILTER_TAPS - 1) of signed(DATA_WIDTH - 1 downto 0);
signal areg_s  : input_registers := (others=>(others=>'0'));

type mult_registers is array(0 to FILTER_TAPS - 1) of signed( (COEFF_WIDTH + DATA_WIDTH - 1) downto 0);
signal mreg_s : mult_registers := (others=>(others=>'0'));

type dsp_registers is array(0 to FILTER_TAPS) of signed( (FIR_FILTER_OUT_WIDTH - 1) downto 0);
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

signal coeff_data : DATA_TYPE := initFromFile(COEFFS_FILE);

-- Behavioral --
begin  
data_o <= std_logic_vector(preg_s(0));         
      
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
                    preg_s(i) <= mreg_s(i) + preg_s(i+1);
                    
                end loop; 
            end if;            
        
        end if;
        
    end process;
    
end Behavioral;
