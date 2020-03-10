#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cells = [Cell(i, arduino) for i in range(1,num_cells+1)]

while True:
    for idx, cell in enumerate(cells):
        x = int(input("angle c" + str(idx+1) + "? "))
        cell.rotate_to_rel_angle(x)
