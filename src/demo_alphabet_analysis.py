#! /usr/bin/python3
import time
start = time.time()
import characters
import random
from cell import *
from arduino import *

arduino = Arduino()
time.sleep(2)
num_cells = arduino.discover()
cell = Cell(1, arduino)

chars = list("abcdefghijklmnopqrstuvwxyz")
results = []

start_tests = time.time()

for i in range(100):
    degrees_sum = 0
    for letter in random.sample(chars, len(chars)):
        big_angle, small_angle = cell.print_character(letter, rotate=False)
        degrees_sum += abs(big_angle) + abs(small_angle)
    results.append(degrees_sum)

print(results)
print(sum(results))
print(sum(results) / len(results))

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
