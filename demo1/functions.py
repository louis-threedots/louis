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

catch_pos = 360 # used as global but will be class property
m=ev3.LargeMotor ('outA')
b=ev3.TouchSensor('in1')

def rotate(m, letter):
        global catch_pos
        reset_pins(m)
        degrees = get_degrees(letter)
        rotate_big_to_angle(m,degrees[0])
        rotate_small_to_angle(m,degrees[1])

def rotate_big_to_angle(m,x):
        global catch_pos
        print("Turning big disc to angle:", x)
        if x > m.position_sp:
            angle = x - m.position_sp
        else:
            angle = 360 - m.position_sp + x
        rotate_to_rel_angle(m,angle)
        catch_pos = m.position_sp
        print("catch_pos: ", catch_pos)

def rotate_small_to_angle(m,x):
        print("Turning small disc to angle:", x)
        if x < m.position_sp:
            angle = x - m.position_sp
        else:
            angle = - m.position_sp - x
        rotate_to_rel_angle(m,angle)

def rotate_to_angle(m,x):
        print("Turning to angle:", x)
        m.run_to_abs_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(4)

def rotate_to_rel_angle(m,x):
        print("Turning to rel angle", x)
        print("pos: ", m.position_sp, m.position)
        m.run_to_rel_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0)
        time.sleep(4)
        print("pos: ", m.position_sp, m.position)
        # weird bug: m.position_sp = 225 before a -255 turn, then afterwards m.position_sp = -225
        # fix it by taking m.position instead of m.position_sp in this assignment:
        m.position_sp = m.position % 360
        print("pos: ", m.position_sp, m.position)

def reset_pins(m):
        if catch_pos > m.position_sp:
            angle = catch_pos - m.position_sp
        else:
            angle = 360 - m.position_sp + catch_pos
        rotate_to_rel_angle(m, angle)

def get_degrees(letter):
    degrees = characters.character_degrees(letter)
    if degrees[1] > degrees[0]:
            degrees[1] -= 360
    return degrees
