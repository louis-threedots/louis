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
                rotate(m, letter)
                print("\n :) !!Printed letter: ", letter, "\n",
                    characters.characters[letter], "\n")

        end = time.time()
        print("\nTime program:" + str(end - start_tests))
        print("Time total:" + str(end - start))
