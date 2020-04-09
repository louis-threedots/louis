#! /usr/bin/python3
import time
start = time.time()
import random
from mainApp import MainApp

chars = list("abcdefghijklmnopqrstuvwxyz")
results = []

mainApp = MainApp()

start_tests = time.time()

for i in range(1000):
    degrees_sum = 0
    alphabetStr = random.sample(chars, len(chars))
    for letter in alphabetStr:
        big_angle, small_angle = mainApp.cells[0].print_character(letter, rotate=False)
        degrees_sum += abs(big_angle) + abs(small_angle)
    results.append(degrees_sum)

print(sum(results) / len(results))

end = time.time()
print('{0:.4g}'.format(end - start_tests))
print("\nTime program:" + str(end - start_tests))
print("Time total:" + str(end - start))
