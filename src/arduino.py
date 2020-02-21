
import serial
import ev3dev.ev3 as ev3
import time

class Arduino:

    def __init__(self):
        # self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.motor = ev3.LargeMotor('outA')

    def discover(self):
        # [cell number, command, data1, data2]
        # Command 0: Cell Discovery
        self.ser.write(bytearray([255,0,0,1]), 'utf-8')
        while True :
            try:
                state=ser.read(4)
                print(state)
            except:
                pass


        return 4 # number of cells


    def run_to_rel_pos(self, rel_angle, cell_index):
        if rel_angle >= 0:
            self.motor.run_to_rel_pos(position_sp = rel_angle, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            # self.ser.write(bytearray([cell_index,1,0,0]), 'utf-8')
        else:
            self.motor.run_to_rel_pos(position_sp = rel_angle, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            # self.ser.write(bytearray([cell_index,2,0,0]), 'utf-8')

        self.motor.wait_until('holding')
        time.sleep(0.4)
