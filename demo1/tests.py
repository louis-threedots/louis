#! /usr/bin/python3
from functions import *

if not (m.connected):
        print ('Plug a motor into port A')
else:
        start_tests = time.time()

        for letter in "abcdefghijklmnopqrstuvwxyz":
                print('Ready for next letter')
                while not b.is_pressed:
                        pass
                reset_pins(m)
                degrees = get_degrees(letter)
                rotate_to_angle(m,degrees[0])
                rotate_to_angle(m,degrees[1])
                print("\n :) !!Printed letter: ", letter, "\n",
                    characters.characters[letter], "\n")

        end = time.time()
        print("\nTime program:" + str(end - start_tests))
        print("Time total:" + str(end - start))
