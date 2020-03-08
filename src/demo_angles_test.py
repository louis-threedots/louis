#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cells = [Cell(i, arduino) for i in range(1,num_cells+1)]

x = 22.5
while True:
    print('Ready for next angle')
    cells[0].wait_for_button_press()
    for cell in reversed(cells):
        cell.rotate_to_rel_angle(x)
