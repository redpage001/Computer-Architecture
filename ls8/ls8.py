#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

print(sys.argv)
if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    print("usage: ls8.py filename")
    sys.exit()
print("FILENAME:",filename)
    
print(filename)

cpu = CPU()

cpu.load()
cpu.run()