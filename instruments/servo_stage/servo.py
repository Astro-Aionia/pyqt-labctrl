import time
import serial

class Servo:
    def __init__(self, port, baud=115200, timeout=1):
        self.port = port
        self.baud = baud
        self.timout = timeout
    def connect(self):
        self.ser = serial.Serial(self.port,baudrate=self.baud,timeout=self.timout)
        print("servo stage is connected. PORT: {port}".format(port=self.port))
        return True
    def disconnect(self):
        self.ser.close()
        print("servo stage is disconnected.")
        return True
    def cmd(self, command, sleep=10):
        self.ser.write(command.encode('ascii'))
        print(self.ser.readline())
        time.sleep(sleep)
        return True
    def home(self):
        print("start homing ...")
        self.cmd('HOMECMD\r',sleep=45)
        print('done.')
        return True
    def moveabs(self, pos, vel=float(30), sleep=10):
        pos = float(pos)
        print("moving to {pos}".format(pos=pos))
        self.cmd("MOVEABS {pos} {vel}\r".format(pos=pos, vel=vel), sleep=sleep)
        print('done.')
        return True
    def moveinc(self, pos=5, vel=float(30), sleep=10):
        pos = float(pos)
        print("moving by {pos}".format(pos=pos))
        self.cmd("MOVEINC {pos} {vel}\r".format(pos=pos, vel=vel), sleep=sleep)
        print('done.')
        return True