## Makefile

# Defaults
SIM ?= modelsim
TOPLEVEL_LANG ?= vhdl
COEFFS_FILE=../data/test_simple_fir.data

# Sources
VHDL_SOURCES += $(PWD)/../hdl/fir_pkg.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_saturator.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_filter.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_top.vhd

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
# TOPLEVEL = fir_saturator
# TOPLEVEL = fir_filter
TOPLEVEL = fir_top

# MODULE is the basename of the Python test file
# MODULE = test_fir_filter
MODULE = test_fir_top

# SIM_ARGS += -gCOEFFS_FILE=$(COEFFS_FILE) 

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
