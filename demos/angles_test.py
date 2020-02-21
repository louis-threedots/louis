#! /usr/bin/python3
import time
start = time.time()
from cell import *

c = Cell(1, Arduino())

if not (c.motor.connected):
        print ('Plug a motor into port A')
else:
        x = 0
        while True:
            print('Ready for next angle')
            while not c.button.is_pressed:
                    pass
            c.rotate_to_angle(x)
            x += 22.5
