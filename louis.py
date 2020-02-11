#! /usr/bin/python3
import time
start = time.time()
from cell import *

c = Cell('A', '1')

if not (c.motor.connected):
        print ('Plug a motor into port A')
else:
        start_louis = time.time()

        for letter in ['l', 'ou', 'i', 's']:
                print('Ready for next letter')
                while not c.button.is_pressed:
                        pass
                c.rotate(letter)
                print("\n :) !!Printed letter: ", letter,"\n")

        end = time.time()
        print("\nTime program:" + str(end - start_louis))
        print("Time total:" + str(end - start))
