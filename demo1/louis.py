#! /usr/bin/python3
import ev3dev.ev3 as ev3
import time
import characters
m=ev3.LargeMotor ('outA')
b=ev3.TouchSensor('in1')

def rotate_to_angle(m,x):
        print("Turning to angle:", x)
        m.run_to_abs_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(3)
def rotate_to_rel_angle(m,x):
        print("Turning to rel angle", x)
        m.run_to_rel_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(3)

def reset_pins(m):
        rotate_to_angle(m, 360)
        m.reset()

if not (m.connected):
        print ('Plug a motor into port A')
else:
        for letter in ['l', 'ou', 'i', 's']:
                print('Ready for next letter')
                while not b.is_pressed:
                        pass
                reset_pins(m)
                degrees = characters.character_degrees(letter)
                rotate_to_angle(m,degrees[0])
                if degrees[1] > degrees[0]:
                        degrees[1] -= 360
                rotate_to_angle(m,degrees[1])
                print("\n :) !!Printed letter: ", letter,"\n")
