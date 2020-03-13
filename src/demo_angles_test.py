#! /usr/bin/python3
import time
start = time.time()
from cell import *

from main_functions import discover
arduino, cells = discover()

x = 22.5
while True:
    print('Ready for next angle')
    cells[0].wait_for_button_press()
    for cell in reversed(cells):
        cell.rotate_to_rel_angle(x)
