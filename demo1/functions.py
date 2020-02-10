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

CATCH_OFFSET = 20

catch = {'position': 360, 'clockwise': 1} # used as global but will be class property
m=ev3.LargeMotor ('outA')
b=ev3.TouchSensor('in1')

def rotate(m, letter):
        global catch, CATCH_OFFSET
        degrees = get_degrees(letter)
        score_clockwise = [
            (catch['position'] + catch['clockwise'] - m.position_sp) % 360 - catch['clockwise'],
            (degrees[0] - catch['position']) % 360,
            (degrees[0] - degrees[1] - catch['clockwise']) % 360 + catch['clockwise']
        ]
        score_anti_clockwise = [
            (m.position_sp - catch['position'] - catch['clockwise']) % 360 + catch['clockwise'] - CATCH_OFFSET,
            (catch['position'] - degrees[0]) % 360,
            (degrees[1] - degrees[0] + catch['clockwise']) % 360 - CATCH_OFFSET - catch['clockwise']
        ]
        print("(", m.position_sp, "-", catch['position'], "-", catch['clockwise'], ") % 360 + ", catch['clockwise'])
        print("(", catch['position'], "-", degrees[0], ") % 360 - ", CATCH_OFFSET)
        print("(", degrees[1], "-", degrees[0], ") % 360 - ", CATCH_OFFSET)
        print("Final values: ", sum(score_clockwise), sum(score_anti_clockwise))
        print("Clockwise: ", score_clockwise)
        print("Anti-clockwise: ", score_anti_clockwise)

        if sum(score_clockwise) <= sum(score_anti_clockwise):
            small_angle = - score_clockwise[2]
            if(score_clockwise[1] == 0): # big disc already in correct position
                big_angle = 0
                small_angle += score_clockwise[0]
            else:
                big_angle = score_clockwise[0] + score_clockwise[1]
        else:
            small_angle = score_anti_clockwise[2]
            if(score_anti_clockwise[1] == 0): # big disc already in correct position
                big_angle = 0
                small_angle -= score_anti_clockwise[0]
            else:
                big_angle = - score_anti_clockwise[0] - score_anti_clockwise[1]

        print(big_angle, small_angle)

        if big_angle != 0:
            rotate_big_to_angle(m, big_angle)
        set_catch(small_angle)
        if small_angle != 0:
            rotate_small_to_angle(m, small_angle)

def rotate_big_to_angle(m, x):
        print("Turning big disc to angle:", x)

        rotate_to_rel_angle(m, x)
        catch['position'] = m.position_sp
        if x < 0:
            catch['position'] -= CATCH_OFFSET

def set_catch(x):
    global catch
    if x > 0:
        catch['clockwise'] = -1
    else:
        catch['clockwise'] = 1
    print(catch)

def rotate_small_to_angle(m, x):
        print("Turning small disc to angle:", x)

        rotate_to_rel_angle(m, x)

def rotate_to_angle(m,x):
        print("Turning to angle:", x)
        m.run_to_abs_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 20)
        m.wait_while('running')
        time.sleep(0.2)

def rotate_to_rel_angle(m,x):
        print("Turning to rel angle", x)
        print("pos: ", m.position_sp, m.position)
        m.run_to_rel_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 20)
        m.wait_while('running')
        time.sleep(0.2)
        print("pos: ", m.position_sp, m.position)
        # weird bug: m.position_sp = 225 before a -255 turn, then afterwards m.position_sp = -225
        # fix it by taking m.position instead of m.position_sp in this assignment:
        m.position_sp = m.position % 360
        print("pos: ", m.position_sp, m.position)

def reset_pins(m):
        if catch['position'] > m.position_sp:
            angle = catch['position'] - m.position_sp
        else:
            angle = 360 - m.position_sp + catch['position']
        rotate_to_rel_angle(m, angle)

def get_degrees(letter):
    degrees = characters.character_degrees(letter)

    return degrees
