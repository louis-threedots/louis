#! /usr/bin/python3
import time
start = time.time()
import characters
from cell import *

# TO RUN ON EV3:
#1
# cd into directory
#2
# to copy files from directory over to EV3
# execute with EV3's IP-address between '@' and ':'
#   scp __init__.py cell.py characters.py louis.py motor_run.py tests.py robot@192.168.105.1:/home/robot
# enter 'maker' as pw
#3
# to connect to EV3
# execute with EV3's IP-address after '@'
#   ssh robot@192.168.105.1
#4
# to run file
# execute
#   ./[filename]

c = Cell(1, Arduino())

if not (c.motor.connected):
        print ('Plug a motor into port A')
else:
        start_tests = time.time()

        for letter in "abcdefghijklmnopqrstuvwxyz":
                print('Ready for next letter')
                while not c.button.is_pressed:
                        pass
                c.rotate(letter)
                print("\n :) !!Printed letter: ", letter, "\n",
                    characters.characters[letter], "\n")

        end = time.time()
        print("\nTime program:" + str(end - start_tests))
        print("Time total:" + str(end - start))
