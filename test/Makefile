## Makefile

# Defaults
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# Sources
VHDL_SOURCES += $(PWD)/../hdl/example.vhd

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = parallel_fir_filter

# MODULE is the basename of the Python test file
MODULE = test_example

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim
