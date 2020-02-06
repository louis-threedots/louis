#! /usr/bin/python3
import time
start = time.time()
import ev3dev.ev3 as ev3
import characters

# TO RUN ON EV3:
#1
# cd into directory
#2
# to copy files from directory over to EV3
# execute with EV3's IP-address between '@' and ':'
#   scp * robot@192.168.105.1:/home/robot
# enter 'maker' as pw
#3
# to connect to EV3
# execute with EV3's IP-address after '@'
#   ssh robot@192.168.105.1
#4
# to run file
# execute
#   ./[filename]

m=ev3.LargeMotor ('outA')
b=ev3.TouchSensor('in1')
catch_pos = 360

def rotate_to_angle(m,x):
        print("Turning to angle:", x)
        m.run_to_abs_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(4)
def rotate_to_rel_angle(m,x):
        print("Turning to rel angle", x)
        m.run_to_rel_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(4)

def reset_pins(m):
        rotate_to_angle(m, 360)
        m.reset()

def get_degrees(letter):
    degrees = characters.character_degrees(letter)
    if degrees[1] > degrees[0]:
            degrees[1] -= 360
    return degrees
