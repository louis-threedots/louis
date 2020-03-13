#! /usr/bin/python3
import time
start = time.time()

# TO RUN ON EV3:
#1
# cd into directory
#2
# to copy files from directory over to EV3
# execute with EV3's IP-address between '@' and ':'
#   scp *.py robot@192.168.105.1:/home/robot
# enter 'maker' as pw
#3
# to connect to EV3
# execute with EV3's IP-address after '@'
#   ssh robot@192.168.105.1
#4
# to make file executable, change the chmod 600 to 700
# execute
#   sudo chmod 700 [filename]
#5
# to run file
# execute
#   ./[filename]

from main_functions import discover
arduino, cells = discover()

start_tests = time.time()

for letter in "abcdefghijklmnopqrstuvwxyz":
        print('Ready for next letter')
        cells[0].wait_for_button_press()
        for cell in reversed(cells):
            cell.print_character(letter)

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
