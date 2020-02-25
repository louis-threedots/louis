#! /usr/bin/python3
import time
start = time.time()
from louis.src.cell import *
from louis.src.arduino import *

c = Cell(1, Arduino())

while True:
        x = int(input("angle? "))
        c.rotate_to_rel_angle(x)
        resetstr = input("want to reset?")
        if resetstr == 'y':
                c.motor_position = 0
                # c.arduino.motor.reset()
#for x in [0,45,90,135,180,225,45]:
#       c.rotate_to_angle(x)
