#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

c = Cell(1, Arduino())

x = 0
while True:
    print('Ready for next angle')
    while not c.button.is_pressed:
            pass
    c.rotate_to_angle(x)
    x += 22.5
