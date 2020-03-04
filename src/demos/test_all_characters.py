#! /usr/bin/python3
import time
start = time.time()
import characters
from cell import *
from arduino import *

# TO RUN ON EV3:
#1
# cd into directory
#2
# to copy files from directory over to EV3
# execute with EV3's IP-address between '@' and ':'
#   scp src/arduino.py src/cell.py src/characters.py src/demos/__init__.py src/demos/angles_test.py src/demos/louis.py src/demos/motor_run.py src/demos/test_all_characters.py robot@192.168.105.1:/home/robot
# enter 'maker' as pw
#3
# to connect to EV3
# execute with EV3's IP-address after '@'
#   ssh robot@192.168.105.1
#4
# to run file
# execute
#   ./[filename]

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cells = [Cell(i, arduino) for i in range(1,num_cells+1)]

start_tests = time.time()

for letter in "abcdefghijklmnopqrstuvwxyz":
        print('Ready for next letter')
        cells[0].arduino.get_pressed_button()
        for cell in reversed(cells):
            cell.print_character(letter)
        print("\n :) !!Printed letter: ", letter, "\n",
            characters.characters[letter], "\n")

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))