#! /usr/bin/python3
import time
start = time.time()

from main_functions import discover
arduino, cells = discover()

while True:
    for idx, cell in enumerate(cells):
        x = int(input("angle c" + str(idx+1) + "? "))
        cell.rotate_to_rel_angle(x)
