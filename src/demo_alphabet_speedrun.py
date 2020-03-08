#! /usr/bin/python3
import time
start = time.time()
import characters
from cell import *
from arduino import *

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cells = [Cell(i, arduino) for i in range(1,num_cells+1)]

start_tests = time.time()

for letter in "abcdefghijklmnopqrstuvwxyz":
        for cell in reversed(cells):
            cell.print_character(letter)

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
