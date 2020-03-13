#! /usr/bin/python3
import time
start = time.time()
from cell import *

from main_functions import discover
arduino, cells = discover()

start_louis = time.time()

for letter in ['l', 'ou', 'i', 's']:
        print('Ready for next letter')
        cells[0].wait_for_button_press()
        for cell in reversed(cells):
            cell.print_character(letter)

end = time.time()
print("\nTime program:" + str(end - start_louis))
print("Time total:" + str(end - start))
