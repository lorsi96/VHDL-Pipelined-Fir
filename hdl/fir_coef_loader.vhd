library ieee;
use ieee.std_logic_1164.ALL;
use ieee.numeric_std.ALL;
use std.textio.all;

library work;
use work.fir_pkg.all;

entity fir_coef_loader is
    generic (
        COEFF_WIDTH : integer := FIR_COEFFICIENT_WIDTH;
        FILTER_TAPS : integer := FIR_MAX_TAPS_N;
        DATA_WIDTH  : integer := FIR_DATA_WIDTH;
        COEFFS_FILE  : string :=  "../data/data_file_init.data"
    );
    port ( 
        coeffs_out     : out fir_coefficients 
    );
end fir_coef_loader;

architecture rtl of fir_coef_loader is
subtype coe_data is bit_vector((COEFF_WIDTH - 1) downto 0);
type DATA_TYPE is array (0 to (FILTER_TAPS - 1)) of coe_data;

impure function initFromFile (data_filename : in string) return fir_coefficients is
    File     DataFile        : text is in data_filename;
    variable DataFileLine    : line;
    variable DATA            : DATA_TYPE;
    variable ret             : fir_coefficients;

    begin
        for i in DATA_TYPE'range loop    
            readline(DataFile, DataFileLine);
            read(DataFileLine, DATA(i));
            ret(i) := signed(to_stdlogicvector(DATA(i)));
        end loop;
    return ret;
end function;

signal coeff_data : fir_coefficients := initFromFile(COEFFS_FILE);

-- rtl --
begin  
    coeffs_out <= coeff_data;
end rtl;
