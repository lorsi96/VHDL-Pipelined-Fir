import os

S1616_MAX = 2**15 - 2**-16
S1616_MIN = -(2**15)
BASE_NAME = "/workspaces/VHDL-Pipelined-Fir/data/data_file_init.data"
DEFAULT_COEF_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), BASE_NAME)
