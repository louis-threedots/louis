#! /usr/bin/python3
import time
import characters

class Cell:

    def __init__(self, index, arduino):
            self.MARGIN = 3
            self.CATCH_SPACING = 90
            self.set_to_default()
            self.arduino = arduino
            self.index = index

    def set_to_default(self):
            self.catch_pos = [0, - self.CATCH_SPACING]
            self.motor_position = 0
            self.big_position = 0
            self.small_position = 0
            self.character = ' '

    def reset(self, to='zero'):
        if to == 'space':
            self.print_character(' ')
        else:
            self.rotate_to_rel_angle(720 - self.motor_position)
            self.set_to_default()

    def get_from_pos_to_catch(self, direction):
        if direction == 'clockwise':
            dist = (self.catch_pos[0] - self.motor_position) % 360
            return self.catch_pos[0], dist
        else:
            dist = (self.motor_position - self.catch_pos[1]) % 360
            return self.catch_pos[1], dist

    def get_optimal_rel_angles(self, letter):
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
                        scores_clockwise.append(
                            {
                                'from_catch_to_big': (clockwise_degrees_big - clockwise_catch_pos) % 360,
                                'from_big_to_small': clockwise_from_big_to_small_degree
                            }
                        )
                    # anticlockwise
                    anti_clockwise_degrees_big = degree_big
                    anti_clockwise_from_big_to_small_degree = (degree_small - degree_big + self.CATCH_SPACING) % 360
                    if anti_clockwise_from_big_to_small_degree <= self.CATCH_SPACING:
                        scores_anti_clockwise.append(
                            {
                                'from_catch_to_big': (anti_clockwise_catch_pos - anti_clockwise_degrees_big + self.CATCH_SPACING) % 360,
                                'from_big_to_small': anti_clockwise_from_big_to_small_degree
                            }
                        )

            idx_min_score_clockwise = scores_clockwise.index(min(scores_clockwise, key=lambda x: sum(x.values())))
            score_clockwise = scores_clockwise[idx_min_score_clockwise]
            score_clockwise['from_pos_to_catch'] = clockwise_from_pos_to_catch

            idx_min_score_anti_clockwise = scores_anti_clockwise.index(min(scores_anti_clockwise, key=lambda x: sum(x.values())))
            score_anti_clockwise = scores_anti_clockwise[idx_min_score_anti_clockwise]
            score_anti_clockwise['from_pos_to_catch'] = anti_clockwise_from_pos_to_catch

            if sum(score_clockwise.values()) <= sum(score_anti_clockwise.values()):
                small_angle = - score_clockwise['from_big_to_small']
                if(abs(score_clockwise['from_catch_to_big']) <= self.MARGIN): # big disc already in correct position
                    big_angle = 0
                    small_angle += score_clockwise['from_pos_to_catch']
                else:
                    self.big_position += score_clockwise['from_catch_to_big']
                    big_angle = score_clockwise['from_pos_to_catch'] + score_clockwise['from_catch_to_big']
            else:
                small_angle = score_anti_clockwise['from_big_to_small']
                if(abs(score_anti_clockwise['from_catch_to_big']) <= self.MARGIN): # big disc already in correct position
                    big_angle = 0
                    small_angle -= score_anti_clockwise['from_pos_to_catch']
                else:
                    self.big_position -= score_anti_clockwise['from_catch_to_big']
                    big_angle = - score_anti_clockwise['from_pos_to_catch'] - score_anti_clockwise['from_catch_to_big']

            self.big_position = self.big_position % 360
            self.small_position += big_angle + small_angle
            self.small_position = self.small_position % 360
            try:
                assert(self.big_position in degrees['big'])
                assert(self.small_position in degrees['small'])
            except:
                print("Believed big-disk position:", str(self.big_position))
                print("Needs to be at one of:")
                print(degrees['big'])
                print("Believed small-disk position:", str(self.small_position))
                print("Needs to be at one of:")
                print(degrees['small'])
                assert(self.big_position in degrees['big'])
                assert(self.small_position in degrees['small'])

            return big_angle, small_angle

    def print_character(self, letter, rotate=True):
            big_angle, small_angle = self.get_optimal_rel_angles(letter)

            if abs(big_angle) > self.MARGIN:
                self.rotate_big_to_angle(big_angle, rotate=rotate)
            if abs(small_angle) > self.MARGIN:
                self.rotate_small_to_angle(small_angle, rotate=rotate)

            self.character = letter

            return big_angle, small_angle

    def rotate_big_to_angle(self, x, rotate=True):
            self.rotate_to_rel_angle(x, rotate=rotate)
            if x < 0:
                self.catch_pos = [(self.motor_position + self.CATCH_SPACING) % 360, self.motor_position]
            else:
                self.catch_pos = [self.motor_position, (self.motor_position - self.CATCH_SPACING) % 360]

    def rotate_small_to_angle(self, x, rotate=True):
            self.rotate_to_rel_angle(x, rotate=rotate)

    def rotate_to_rel_angle(self, x, rotate=True):
            if rotate:
                print("Turning to rel angle", x)
                self.arduino.run_to_rel_pos(x, self.index)
            self.motor_position += x
            self.motor_position = self.motor_position % 360

    def has_finished_rotating(self):
        # Returns true if the cell has finished rendering
        return self.arduino.ping(self.index)

    def wait_for_button_press(self):
        if self.arduino.get_pressed_button() != self.index:
            self.wait_for_button_press()
        return True
        #TODO return False after timeout
