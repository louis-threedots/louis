#! /usr/bin/python3
import time
start = time.time()
import random
from cell import *

from main_functions import discover
arduino, cells = discover()

chars = list("abcdefghijklmnopqrstuvwxyz")
results = []

start_tests = time.time()

for i in range(100):
    degrees_sum = 0
    for letter in random.sample(chars, len(chars)):
        big_angle, small_angle = cells[0].print_character(letter, rotate=False)
        degrees_sum += abs(big_angle) + abs(small_angle)
    results.append(degrees_sum)

print(results)
print(sum(results))
print(sum(results) / len(results))

end = time.time()
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
