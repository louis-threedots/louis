#! /usr/bin/python3
import time
import characters
import ev3dev.ev3 as ev3

class Cell:

    def __init__(self, index, arduino):
            self.margin = 3
            self.catch = {'position': [0, 180], 'clockwise': self.margin}
            self.arduino = arduino
            self.motor_position = 0
            self.index = index
            self.button = ev3.TouchSensor('in' + str(index))
            self.CATCH_OFFSET = 0

    def get_from_pos_to_catch(self, direction):
        pos = {}

        if direction == 'clockwise':
            pos[0] = (self.catch['position'][0] - self.motor_position + self.catch['clockwise']) % 360 - self.catch['clockwise']
            pos[1] = (self.catch['position'][1] - self.motor_position + self.catch['clockwise']) % 360 - self.catch['clockwise']
        else:
            pos[0] = (self.motor_position - self.catch['position'][0] - self.catch['clockwise'] - self.CATCH_OFFSET) % 360 + self.catch['clockwise']
            pos[1] = (self.motor_position - self.catch['position'][1] - self.catch['clockwise'] - self.CATCH_OFFSET) % 360 + self.catch['clockwise']

        if pos[0] < pos[1]:
            return self.catch['position'][0], pos[0]
        else:
            return self.catch['position'][1], pos[1]

    def rotate(self, letter):
            degrees = characters.character_degrees(letter)

            clockwise_catch_pos, clockwise_from_pos_to_catch = self.get_from_pos_to_catch('clockwise')
            anti_clockwise_catch_pos, anti_clockwise_from_pos_to_catch = self.get_from_pos_to_catch('anti_clockwise')

            clockwise_degrees_big = degrees['big'][0]
            clockwise_from_big_to_small_degree = (degrees['big'][0] - degrees['small']) % 360
            if clockwise_from_big_to_small_degree >= 180:
                clockwise_degrees_big = degrees['big'][1]
                clockwise_from_big_to_small_degree = (degrees['big'][1] - degrees['small']) % 360

            anti_clockwise_degrees_big = degrees['big'][0]
            anti_clockwise_from_big_to_small_degree = (degrees['small'] - degrees['big'][0] + self.catch['clockwise'] - self.CATCH_OFFSET) % 360 - self.catch['clockwise']
            if anti_clockwise_from_big_to_small_degree >= 180:
                anti_clockwise_degrees_big = degrees['big'][1];
                anti_clockwise_from_big_to_small_degree = (degrees['small'] - degrees['big'][1] + self.catch['clockwise'] - self.CATCH_OFFSET) % 360 - self.catch['clockwise']

            score_clockwise = {
                'from_pos_to_catch': clockwise_from_pos_to_catch,
                'from_catch_to_big': (clockwise_degrees_big - clockwise_catch_pos) % 360,
                'from_big_to_small': clockwise_from_big_to_small_degree
            }

            score_anti_clockwise = {
                'from_pos_to_catch': anti_clockwise_from_pos_to_catch,
                'from_catch_to_big': (anti_clockwise_catch_pos - anti_clockwise_degrees_big) % 360,
                'from_big_to_small': anti_clockwise_from_big_to_small_degree
            }

            print("\nCLOCKWISE:")
            # print("(", self.catch['position'], "-", self.motor_position, "+", self.catch['clockwise'], ") % 360 - ", self.catch['clockwise'])
            # print("(", degrees['big'], "-", self.catch['position'], ") % 360")
            # print("(", degrees['big'], "-", degrees['small'], ") % 360")
            print("Clockwise: ", score_clockwise)

            print("\nANTI:")
            # print("(", self.motor_position, "-", self.catch['position'], "-", self.catch['clockwise'], "-", self.CATCH_OFFSET, ") % 360 + ", self.catch['clockwise'])
            # print("(", self.catch['position'], "-", degrees['big'], ") % 360")
            # print("(", degrees['small'], "-", degrees['big'], "+", self.catch['clockwise'], "-", self.CATCH_OFFSET, ") % 360 - ", self.catch['clockwise'])
            print("Anti-clockwise: ", score_anti_clockwise)

            print("\nFinal values: ", sum(score_clockwise.values()), sum(score_anti_clockwise.values()), "\n")

            if sum(score_clockwise.values()) <= sum(score_anti_clockwise.values()):
                self.catch['clockwise'] = self.margin

                small_angle = - score_clockwise['from_big_to_small']
                if(abs(score_clockwise['from_catch_to_big']) <= 1): # big disc already in correct position
                    big_angle = 0
                    small_angle += score_clockwise['from_pos_to_catch']
                else:
                    big_angle = score_clockwise['from_pos_to_catch'] + score_clockwise['from_catch_to_big']
            else:
                self.catch['clockwise'] = - self.margin

                small_angle = score_anti_clockwise['from_big_to_small']
                if(abs(score_anti_clockwise['from_catch_to_big']) <= self.margin): # big disc already in correct position
                    big_angle = 0
                    small_angle -= score_anti_clockwise['from_pos_to_catch']
                else:
                    big_angle = - score_anti_clockwise['from_pos_to_catch'] - score_anti_clockwise['from_catch_to_big']

            if abs(big_angle) > self.margin:
                self.rotate_big_to_angle(big_angle)
            if abs(small_angle) > self.margin:
                self.rotate_small_to_angle(small_angle)

    def rotate_big_to_angle(self, x):
            print("Turning big disc to angle:", x)

            self.rotate_to_rel_angle(x)

            self.catch['position'] = [self.motor_position, (self.motor_position + 180) % 360]
            if x < 0:
                self.catch['position'][0] -= self.CATCH_OFFSET
                self.catch['position'][1] -= self.CATCH_OFFSET

    def rotate_small_to_angle(self, x):
            print("Turning small disc to angle:", x)

            self.rotate_to_rel_angle(x)

    def rotate_to_angle(self, x):
            print("Turning to angle:", x)
            print("NOT WORKING FOR ARDUINO")
            # self.motor.run_to_abs_pos(position_sp = x, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            # self.motor.wait_until('holding')
            # time.sleep(0.4)

    def rotate_to_rel_angle(self, x):
            print("Turning to rel angle", x)
            print("pos: ", self.motor_position)
            self.arduino.run_to_rel_pos(x, self.index)
            self.motor_position += x
            self.motor_position = self.motor_position % 360
            print("pos: ", self.motor_position)
