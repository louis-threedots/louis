#! /usr/bin/python3
from functions import *

if not (m.connected):
        print ('Plug a motor into port B')
else:
        while True:
                x = int(input("angle? "))
                rotate_to_angle(m,x)
                resetstr = input("want to reset?")
                if resetstr == 'y':
                        m.reset()
        #for x in [0,45,90,135,180,225,45]:
        #       rotate_to_angle(m,x)
        #       print(m.position_sp)
