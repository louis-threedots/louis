#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cells = [Cell(i, arduino) for i in range(1,num_cells+1)]

start_louis = time.time()

for letter in ['l', 'ou', 'i', 's']:
        print('Ready for next letter')
        cells[0].wait_for_button_press()
        for cell in reversed(cells):
            cell.print_character(letter)
        print("\n :) !!Printed letter: ", letter,"\n")

end = time.time()
print("\nTime program:" + str(end - start_louis))
print("Time total:" + str(end - start))
