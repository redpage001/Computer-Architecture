#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

print(sys.argv)
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Must provide command line argument")
    sys.exit()
print("FILENAME:",filename)
    
print(filename)

cpu = CPU()

cpu.load()
cpu.run()