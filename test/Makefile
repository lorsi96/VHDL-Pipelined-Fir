## Makefile

# Defaults
FIR_TARGET=top
SIM ?= modelsim
TOPLEVEL_LANG ?= vhdl
COEFFS_FILE=../data/voice_filter.data

# Sources
VHDL_SOURCES += $(PWD)/../hdl/fir_pkg.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_saturator.vhd
VHDL_SOURCES += $(PWD)/../hdl/fir_filter.vhd
# VHDL_SOURCES += $(PWD)/../hdl/fir_top.vhd

TOPLEVEL = fir_$(FIR_TARGET)

MODULE = test_fir_$(FIR_TARGET)

# ifeq $COEFFS_FILE 
# SIM_ARGS="-gCOEFFS_FILE=$(COEFFS_FILE)"
# TESTCASE=arbitrary_filter_test

include $(shell cocotb-config --makefiles)/Makefile.sim
