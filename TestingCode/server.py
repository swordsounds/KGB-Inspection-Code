import cv2
import socket
import time
import threading
from PCA9685 import PCA9685
import RPi.GPIO as io
import struct
import pickle
import  pyshine as ps #  pip3 install pyshine==0.0.9
from subprocess import call
HTML="""
<html>
<head>
<title>PyShine Live Streaming</title>
</head>

<body>
<center><h1> PyShine Live Streaming using OpenCV </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""

def main():
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = ('192.168.0.11',9000) # Enter your IP address 
    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()
        
def get_command():
    s = socket.socket()
    s.bind(('192.168.0.11', 8000))
    s.listen(5)
    client_socket,addr = s.accept()
    data = b""
    payload_size = struct.calcsize("Q")
    controller = Controller()
    print(controller.wristLeft)
    arm = RoboArt(controller)
    arm.start()
    
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024) # 4K
                if not packet: break
                data+=packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q",packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            frame_data = data[:msg_size]
            data  = data[msg_size:]
            frame = pickle.loads(frame_data)
            print('',end='\n')
            controller.execute_command(command=frame)
            #print('CLIENT TEXT RECEIVED:',frame,end='\n')
            #print('SERVER TEXT SENDING:')
          

        except Exception as e:
            #print(e)
            pass

    client_socket.close()
    print('Audio closed')

    

class Controller():
    
    
    def __init__(self, queue=None, **kwargs):
        
        self.queue = queue
        self.wristRight = 0
        self.wristLeft = 0
        self.elbowOpen = 0
        self.elbowClose = 0
        self.close = 0
        self.open = 0
        self.wristUp= 0
        self.wristDown = 0
        self.base0Left = 0
        self.base0Right = 0
        self.base1Left = 0
        self.base1Right = 0
        self.gripperClose = 0
        self.gripperOpen = 0
        
        

        

    def execute_command(self, command):
        
        in1 = 12
        in2 = 36
        in3 = 33
        in4 = 35
        basein1 = 13
        basein2 = 15
        elbowin1 = 16
        elbowin2 = 18
        wristin1 = 22
        wristin2 = 29

        io.setmode(io.BOARD)
        io.setwarnings(False)
        io.setup(in1,io.OUT)
        io.setup(in2,io.OUT)
        io.setup(in3,io.OUT)
        io.setup(in4,io.OUT)
        io.setup(basein1,io.OUT)
        io.setup(basein2,io.OUT)
        io.setup(elbowin1,io.OUT)
        io.setup(elbowin2,io.OUT)
        io.setup(wristin1,io.OUT)
        io.setup(wristin2,io.OUT)
        
        commands = command.split(' ')
        #print(command)
        
        if command == 'shutdowncrawler':
            call("sudo shutdown -h now", shell=True)
        
        self.wristLeft = (int(commands[0]) * (-1) / 32767.0)
        self.wristRight = (int(commands[1]) / 32767.0)
        self.gripperClose = int(commands[2])
        self.gripperOpen = int(commands[3])
        io.output(in1,int(commands[4]))
        io.output(in2,int(commands[5]))
        io.output(in3,int(commands[6]))
        io.output(in4,int(commands[7]))
        io.output(basein1,int(commands[8]))
        io.output(basein2,int(commands[9]))
        io.output(elbowin1,int(commands[10]))
        io.output(elbowin2,int(commands[11]))
        io.output(wristin1,int(commands[12]))
        io.output(wristin2,int(commands[13]))

        

class RoboArt(threading.Thread):

    S0_IN = 500
    S0_OUT = 2000
    S1_OUT = 1450
    S1_IN = 900
    
    


    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.driver = PCA9685(0x40, debug=False)
        self.driver.setPWMFreq(50)
        self._lock = threading.Lock()
        self.controller = controller
        
        

    def check(self, s0, s1):
        if s0 > RoboArt.S0_OUT:
            s0 = RoboArt.S0_OUT
        if s0 < RoboArt.S0_IN:
            s0 = RoboArt.S0_IN
        if s1 > RoboArt.S1_OUT:
            s1 = RoboArt.S1_OUT
        if s1 < RoboArt.S1_IN:
            s1 = RoboArt.S1_IN
        return s0, s1

    def run(self):
        servo0 = 1000
        servo1 = 1000
        while True:
            if self.controller.wristLeft > 0:
                servo0 += int(25 * self.controller.wristLeft)
            elif self.controller.wristRight > 0:
                servo0 -= int(25 * self.controller.wristRight)
            if self.controller.gripperClose > 0:
                servo1 += int(25 * self.controller.gripperClose)
            elif self.controller.gripperOpen > 0:
                servo1 -= int(25 * self.controller.gripperOpen)

            servo0, servo1 = self.check(servo0, servo1)
            self.driver.setServoPulse(0, servo0)
            self.driver.setServoPulse(1, servo1)
            time.sleep(0.025)



if __name__=='__main__':
    t1 = threading.Thread(target=main, args=())
    t2 = threading.Thread(target=get_command, args=())
    t1.start()
    t2.start()
    