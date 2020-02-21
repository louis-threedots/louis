
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
