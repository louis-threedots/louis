#! /usr/bin/python3
import time
import ev3dev.ev3 as ev3
import characters

class Cell:

    def __init__(self, motorPort, buttonPort):
            self.catch = {'position': 360, 'clockwise': 1}
            self.motor = ev3.LargeMotor('out' + str(motorPort))
            self.button = ev3.TouchSensor('in' + str(buttonPort))
            self.CATCH_OFFSET = 20

    def rotate(self, letter):
            degrees = self.get_degrees(letter)

            score_clockwise = {
                'from_pos_to_catch': (self.catch['position'] - self.motor.position_sp + self.catch['clockwise']) % 360 - self.catch['clockwise'],
                'from_catch_to_big': (degrees[0] - self.catch['position']) % 360,
                'from_big_to_small': (degrees[0] - degrees[1]) % 360
            }
            score_anti_clockwise = {
                'from_pos_to_catch': (self.motor.position_sp - self.catch['position'] - self.catch['clockwise'] - self.CATCH_OFFSET) % 360 + self.catch['clockwise'],
                'from_catch_to_big': (self.catch['position'] - degrees[0]) % 360,
                'from_big_to_small': (degrees[1] - degrees[0] + self.catch['clockwise'] - self.CATCH_OFFSET) % 360 - self.catch['clockwise']
            }

            print("\nCLOCKWISE:")
            print("(", self.catch['position'], "-", self.motor.position_sp, "+", self.catch['clockwise'], ") % 360 - ", self.catch['clockwise'])
            print("(", degrees[0], "-", self.catch['position'], ") % 360")
            print("(", degrees[0], "-", degrees[1], ") % 360")
            print("Clockwise: ", score_clockwise)

            print("\nANTI:")
            print("(", self.motor.position_sp, "-", self.catch['position'], "-", self.catch['clockwise'], "-", self.CATCH_OFFSET, ") % 360 + ", self.catch['clockwise'])
            print("(", self.catch['position'], "-", degrees[0], ") % 360")
            print("(", degrees[1], "-", degrees[0], "+", self.catch['clockwise'], "-", self.CATCH_OFFSET, ") % 360 - ", self.catch['clockwise'])
            print("Anti-clockwise: ", score_anti_clockwise)

            print("\nFinal values: ", sum(score_clockwise.values()), sum(score_anti_clockwise.values()), "\n")

            if sum(score_clockwise.values()) <= sum(score_anti_clockwise.values()):
                self.catch['clockwise'] = 1

                small_angle = - score_clockwise['from_big_to_small']
                if(score_clockwise['from_catch_to_big'] == 0): # big disc already in correct position
                    big_angle = 0
                    small_angle += score_clockwise['from_pos_to_catch']
                else:
                    big_angle = score_clockwise['from_pos_to_catch'] + score_clockwise['from_catch_to_big']
            else:
                self.catch['clockwise'] = -1

                small_angle = score_anti_clockwise['from_big_to_small']
                if(score_anti_clockwise['from_catch_to_big'] == 0): # big disc already in correct position
                    big_angle = 0
                    small_angle -= score_anti_clockwise['from_pos_to_catch']
                else:
                    big_angle = - score_anti_clockwise['from_pos_to_catch'] - score_anti_clockwise['from_catch_to_big']

            print(big_angle, small_angle)

            if big_angle != 0:
                self.rotate_big_to_angle(big_angle)
            if small_angle != 0:
                self.rotate_small_to_angle(small_angle)

    def rotate_big_to_angle(self, x):
            print("Turning big disc to angle:", x)

            self.rotate_to_rel_angle(x)

            self.catch['position'] = self.motor.position_sp
            if x < 0:
                self.catch['position'] -= self.CATCH_OFFSET

    def rotate_small_to_angle(self, x):
            print("Turning small disc to angle:", x)

            self.rotate_to_rel_angle(x)

    def rotate_to_angle(self, x):
            print("Turning to angle:", x)
            self.motor.run_to_abs_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 20)
            self.motor.wait_until('holding')
            time.sleep(0.2)

    def rotate_to_rel_angle(self, x):
            print("Turning to rel angle", x)
            print("pos: ", self.motor.position_sp, self.motor.position)
            self.motor.run_to_rel_pos(position_sp = x, speed_sp = 150, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 20)
            self.motor.wait_until('holding')
            time.sleep(0.2)
            print("pos: ", self.motor.position_sp, self.motor.position)
            # weird bug: self.motor.position_sp = 225 before a -255 turn, then afterwards self.motor.position_sp = -225
            # fix it by taking self.motor.position instead of self.motor.position_sp in this assignment:
            self.motor.position_sp = self.motor.position % 360
            print("pos: ", self.motor.position_sp, self.motor.position)

    def get_degrees(self, letter):
        degrees = characters.character_degrees(letter)

        return degrees
