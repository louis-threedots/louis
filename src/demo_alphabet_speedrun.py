#! /usr/bin/python3
import time
start = time.time()
from cell import *

from main_functions import discover
arduino, cells = discover()

start_tests = time.time()

for letter in "abcdefghijklmnopqrstuvwxyz":
        for cell in reversed(cells):
            cell.print_character(letter)

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
