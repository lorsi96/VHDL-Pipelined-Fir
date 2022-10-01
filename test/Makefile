## Makefile

# Defaults
SIM ?= modelsim
TOPLEVEL_LANG ?= vhdl

# Sources
VHDL_SOURCES += $(PWD)/../hdl/fir_pkg.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_saturator.vhd

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = fir_saturator

# MODULE is the basename of the Python test file
MODULE = test_fir_saturator

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
