#! /usr/bin/python3
import time
import characters
#import ev3dev.ev3 as ev3

class Cell:

    def __init__(self, index, arduino):
            self.MARGIN = 3
            self.CATCH_SPACING = 90
            self.catch_pos = [0, - self.CATCH_SPACING]
            self.arduino = arduino
            self.motor_position = 0
            self.index = index

    def get_from_pos_to_catch(self, direction):
        if direction == 'clockwise':
            dist = (self.catch_pos[0] - self.motor_position) % 360
            return self.catch_pos[0], dist
        else:
            dist = (self.motor_position - self.catch_pos[1]) % 360
            return self.catch_pos[1], dist

    def print_character(self, letter):
            degrees = characters.character_degrees(letter)

            clockwise_catch_pos, clockwise_from_pos_to_catch = self.get_from_pos_to_catch('clockwise')
            anti_clockwise_catch_pos, anti_clockwise_from_pos_to_catch = self.get_from_pos_to_catch('anti_clockwise')

            scores_clockwise = []
            scores_anti_clockwise = []

            for i, degree_small in enumerate(degrees['small']):
                for j, degree_big in enumerate(degrees['big']):
                    # clockwise
                    clockwise_degrees_big = degree_big
                    clockwise_from_big_to_small_degree = (degree_big - degree_small) % 360
                    if clockwise_from_big_to_small_degree <= self.CATCH_SPACING:
                        print('clockwise')
                        print('from_catch_to_big: (', str(clockwise_degrees_big), '-', str(clockwise_catch_pos), ') % 360 = ', str((clockwise_degrees_big - clockwise_catch_pos) % 360))
                        print('from_big_to_small: ', str(clockwise_from_big_to_small_degree))
                        scores_clockwise.append(
                            {
                                'from_catch_to_big': (clockwise_degrees_big - clockwise_catch_pos) % 360,
                                'from_big_to_small': clockwise_from_big_to_small_degree
                            }
                        )
                    # anticlockwise
                    anti_clockwise_degrees_big = degree_big
                    anti_clockwise_from_big_to_small_degree = (degree_small - degree_big) % 360
                    if anti_clockwise_from_big_to_small_degree <= self.CATCH_SPACING:
                        print('anticlockwise')
                        print('from_catch_to_big: (', str(anti_clockwise_catch_pos), '-', str(anti_clockwise_degrees_big), ') % 360 = ', str((anti_clockwise_catch_pos - anti_clockwise_degrees_big) % 360))
                        print('from_big_to_small: ', str(anti_clockwise_from_big_to_small_degree))
                        scores_anti_clockwise.append(
                            {
                                'from_catch_to_big': (anti_clockwise_catch_pos - anti_clockwise_degrees_big) % 360,
                                'from_big_to_small': anti_clockwise_from_big_to_small_degree
                            }
                        )

            print('')
            print(self.motor_position)
            print('clockwise_from_pos_to_catch: ', str(clockwise_from_pos_to_catch))
            print(scores_clockwise)
            print('anti_clockwise_from_pos_to_catch: ', str(anti_clockwise_from_pos_to_catch))
            print(scores_anti_clockwise)
            print('')

            idx_min_score_clockwise = scores_clockwise.index(min(scores_clockwise, key=lambda x: sum(x.values())))
            score_clockwise = scores_clockwise[idx_min_score_clockwise]
            score_clockwise['from_pos_to_catch'] = clockwise_from_pos_to_catch

            idx_min_score_anti_clockwise = scores_anti_clockwise.index(min(scores_anti_clockwise, key=lambda x: sum(x.values())))
            score_anti_clockwise = scores_anti_clockwise[idx_min_score_anti_clockwise]
            score_anti_clockwise['from_pos_to_catch'] = anti_clockwise_from_pos_to_catch

            if sum(score_clockwise.values()) <= sum(score_anti_clockwise.values()):
                small_angle = - score_clockwise['from_big_to_small']
                if(abs(score_clockwise['from_catch_to_big']) <= 1): # big disc already in correct position
                    big_angle = 0
                    small_angle += score_clockwise['from_pos_to_catch']
                else:
                    big_angle = score_clockwise['from_pos_to_catch'] + score_clockwise['from_catch_to_big']
            else:
                small_angle = score_anti_clockwise['from_big_to_small']
                if(abs(score_anti_clockwise['from_catch_to_big']) <= self.MARGIN): # big disc already in correct position
                    big_angle = 0
                    small_angle -= score_anti_clockwise['from_pos_to_catch']
                else:
                    big_angle = - score_anti_clockwise['from_pos_to_catch'] - score_anti_clockwise['from_catch_to_big']

            if abs(big_angle) > self.MARGIN:
                self.rotate_big_to_angle(big_angle)
            if abs(small_angle) > self.MARGIN:
                self.rotate_small_to_angle(small_angle)

            return True

    def rotate_big_to_angle(self, x):
            print("Turning big disc to angle:", x)
            self.rotate_to_rel_angle(x)
            if x < 0:
                self.catch_pos = [(self.motor_position + self.CATCH_SPACING) % 360, self.motor_position]
            else:
                self.catch_pos = [self.motor_position, (self.motor_position - self.CATCH_SPACING) % 360]

    def rotate_small_to_angle(self, x):
            print("Turning small disc to angle:", x)
            self.rotate_to_rel_angle(x)

    def rotate_to_angle(self, x):
            print("Turning to angle:", x)
            self.arduino.motor.run_to_abs_pos(position_sp = x, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            self.arduino.motor.wait_until('holding')
            time.sleep(0.4)

    def rotate_to_rel_angle(self, x):
            print("Turning to rel angle", x)
            self.arduino.run_to_rel_pos(x, self.index)
            self.motor_position += x
            self.motor_position = self.motor_position % 360

    def wait_for_button_press(self):
        if self.arduino.get_pressed_button() != self.index:
            self.wait_for_button_press()
        return True
        #TODO return False after timeout
