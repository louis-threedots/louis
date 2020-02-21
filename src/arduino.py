
import serial
class Arduino:

    def __init__:
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

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
            self.ser.write(bytearray([cell_index,1,0,0]), 'utf-8')
        else:
            self.ser.write(bytearray([cell_index,2,0,0]), 'utf-8')
