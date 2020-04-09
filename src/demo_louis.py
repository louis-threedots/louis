#! /usr/bin/python3
import time
start = time.time()
from mainApp import MainApp

mainApp = MainApp()

start_louis = time.time()

while True:
    for letter in ['l', 'ou', 'i', 's']:
        time.sleep(1)
        for cell in reversed(mainApp.cells):
            cell.print_character(letter)
        mainApp.print_cells_to_terminal()
    cell.reset(' ')
    mainApp.print_cells_to_terminal()

end = time.time()
print("\nTime program:" + str(end - start_louis))
print("Time total:" + str(end - start))
