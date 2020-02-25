#! /usr/bin/python3
import time
start = time.time()
from cell import *
from arduino import *

c = Cell(1, Arduino())
c2 = Cell(2, Arduino())

while True:
    x = int(input("angle c1? "))
    c.rotate_to_rel_angle(x)
    x2 = int(input("angle c2? "))
    c2.rotate_to_rel_angle(x2)
