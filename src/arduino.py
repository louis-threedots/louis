import serial
import time
import ev3dev.ev3 as ev3

class Arduino:

    def __init__(self, main_cell):
        self.main_cell = main_cell
        try:
            try:
                self.ser = serial.Serial('/dev/ttyACM0',9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
            except:
                self.ser = serial.Serial('/dev/ttyACM1',9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
            self.cell_offset = 96
            self.main_cell = 'arduino'
        except:
            self.motor = ev3.MediumMotor('outA')
            if not self.motor.connected:
                self.motor = ev3.LargeMotor('outA')
            if self.motor.connected:
                self.button = ev3.TouchSensor('in1')
                self.main_cell = 'ev3'

    def discover(self):
        if self.main_cell == 'ev3':
            return 1
        elif self.main_cell == 'comp':
            inp = input("How many cells would you like to work with? (integer) ")
            try:
                return int(inp)
            except:
                return self.discover()
        # [cell number, command, data1, data2]
        # Command 0: Cell Discovery
        #self.ser.write(bytearray([255,0,0,1]), )
        self.ser.write(b'acaa')
        #time.sleep(5.0)
        ack=self.ser.read(4) #TODO: Check ack
        discovery_result = self.ser.read(4)
        print(discovery_result)
        return discovery_result[3] - self.cell_offset

    def convert_to_base(self,angle):
        if angle <= 255:
            return [0,angle]
        else:
            return [int(angle/256), angle % 256]

    def run_to_rel_pos(self, rel_angle, cell_index):
        if self.main_cell == 'ev3':
            self.motor.run_to_rel_pos(position_sp = rel_angle, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            if abs(rel_angle) >= 10:
                self.motor.wait_until('holding')
            time.sleep(0.5)
        elif self.main_cell == 'comp':
            return
        else:
            if rel_angle >= 0:
                self.ser.write(bytearray([self.cell_offset+cell_index,102]+self.convert_to_base(rel_angle)))
            else:
                self.ser.write(bytearray([self.cell_offset+cell_index,103]+self.convert_to_base((-1)*rel_angle)))

    def get_pressed_button(self):
        if self.main_cell == 'ev3':
            while not self.button.is_pressed:
                pass
            return 1
        elif self.main_cell == 'comp':
            inp = input("Enter a cell index to imitate a button press: (integer) ")
            try:
                return int(inp)
            except:
                return self.get_pressed_button()
        else:
            #TODO: Add timeout
            self.ser.read(self.ser.inWaiting())
            button_message = self.ser.read(4)
            while button_message[1]!= 105:
                button_message = self.ser.read(4)
            return button_message[3] - self.cell_offset

    def ping(self, cell_index):
        if self.main_cell == 'ev3':
            return True
        elif self.main_cell == 'comp':
            return True
        else:
            #TODO: Add timeout
            self.ser.write(bytearray([self.cell_offset+cell_index,106,0,0]))
            pong = self.ser.read(4)
            while pong[1] != 107 and pong[0] != self.cell_offset+cell_index:
                pong = self.ser.read(4)
            return True
