#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
#   python3 ls8.py examples/mult.ls83  because argv[0] is ls8.py and argv[1] is examples/mult.ls83

# do checks
# check length of arguments
if len(sys.argv) != 2:
    print('wrong number of arguments passed in')
else:
    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()