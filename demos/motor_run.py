#! /usr/bin/python3
import time
start = time.time()
from cell import *

c = Cell(1, Arduino())

if not (c.motor.connected):
        print ('Plug a motor into port A')
else:
        while True:
                x = float(input("angle? "))
                c.rotate_to_angle(x)
                resetstr = input("want to reset?")
                if resetstr == 'y':
                        c.motor.reset()
        #for x in [0,45,90,135,180,225,45]:
        #       c.rotate_to_angle(x)
        #       print(m.position_sp)
