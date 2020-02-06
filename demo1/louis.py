#! /usr/bin/python3
from functions import *

if not (m.connected):
        print ('Plug a motor into port A')
else:
        start_louis = time.time()

        for letter in ['l', 'ou', 'i', 's']:
                print('Ready for next letter')
                while not b.is_pressed:
                        pass
                rotate(m, letter)
                print("\n :) !!Printed letter: ", letter,"\n")

        end = time.time()
        print("\nTime program:" + str(end - start_louis))
        print("Time total:" + str(end - start))
