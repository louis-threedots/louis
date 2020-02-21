#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

c = Cell(1, Arduino())
c2 = Cell(2, Arduino())

start_louis = time.time()

for letter in ['l', 'ou', 'i', 's']:
        print('Ready for next letter')
        while not c.button.is_pressed:
                pass
        c.rotate(letter)
        # c2.rotate(letter)
        print("\n :) !!Printed letter: ", letter,"\n")

while not c.button.is_pressed:
        pass
c.rotate_to_rel_angle(360 - c.motor_position)

end = time.time()
print("\nTime program:" + str(end - start_louis))
print("Time total:" + str(end - start))
