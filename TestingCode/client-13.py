import cv2
import numpy as np
import socket
import struct
import pickle
import threading
import time
#from pyPS4Controller.controller import Controller

class MyController():

    def __init__(self, queue=None, **kwargs):
        #Controller.__init__(self, **kwargs)
        self.queue = queue
        self.wristLeft = 0
        self.wristRight = 0
        self.gripperClose = 0
        self.gripperOpen = 0
        self.in1 = 0
        self.in2 = 0
        self.in3 = 0
        self.in4 = 0
        self.basein1 = 0
        self.basein2 = 0
        self.elbowin1 = 0
        self.elbowin2 = 0
        self.wristin1 = 0
        self.wristin2 = 0
        self.shutdowncrawler = False

    def on_L1_press(self):
        self.gripperClose = 1
        self.gripperOpen = 0

    def on_L1_release(self):
        self.gripperClose = 0
        self.gripperOpen = 0

    def on_R1_press(self):
        self.gripperClose = 0
        self.gripperOpen = 1

    def on_R1_release(self):
        self.gripperClose = 0
        self.gripperOpen = 0

    def on_L3_up(self, value):
        self.basein1 = 1
        self.basein2 = 0
        
    def on_L3_down(self, value):
        self.basein1 = 0
        self.basein2 = 1

    def on_L3_left(self, value):
        self.elbowin1 = 1
        self.elbowin2 = 0

    def on_L3_right(self, value):
        self.elbowin1 = 0
        self.elbowin2 = 1

    def on_L3_x_at_rest(self):
        self.elbowin1 = 0
        self.elbowin2 = 0

    def on_L3_y_at_rest(self):
        self.basein1 = 0
        self.basein2 = 0

    def on_R3_up(self, value):
        self.wristin1 = 1
        self.wristin2 = 0

    def on_R3_down(self, value):
        self.wristin1 = 0
        self.wristin2 = 1

    def on_R3_y_at_rest(self):
        self.wristin1 = 0
        self.wristin2 = 0

    def on_R3_left(self, value):
        self.wristLeft = value
        self.wristRight = 0

    def on_R3_right(self, value):
        self.wristLeft = 0
        self.wristRight = value

    def on_R3_x_at_rest(self):
        self.wristLeft = 0
        self.wristRight = 0

    #move the robot elbowOpen
    def on_up_arrow_press(self):
        self.in1 = 1
        self.in2 = 0
        self.in3 = 0
        self.in4 = 1
        
	#stop the robot	
    def on_up_down_arrow_release(self):
        self.in1 = 0
        self.in2 = 0
        self.in3 = 0
        self.in4 = 0
        
	#move the robot elbowClose
    def on_down_arrow_press(self):
        self.in1 = 0
        self.in2 = 1
        self.in3 = 1
        self.in4 = 0
        
	#move the robot right
    def on_right_arrow_press(self):
        self.in1 = 1
        self.in2 = 0
        self.in3 = 1
        self.in4 = 0
        
	#stop the robot
    def on_left_right_arrow_release(self):
        self.in1 = 0
        self.in2 = 0
        self.in3 = 0
        self.in4 = 0
        
	#move the robot left
    def on_left_arrow_press(self):
        self.in1 = 0
        self.in2 = 1
        self.in3 = 0
        self.in4 = 1




class ControlMessage(threading.Thread):
    
    def __init__(self, controller):
        threading.Thread.__init__(self)
        self._lock = threading.Lock()
        self.controller = controller

    def build(self):
        message = ''
        if self.controller.shutdowncrawler == True:
            message = 'shutdowncrawler'
            self.controller.shutdowncrawler = False
        else:
            message += str(self.controller.wristLeft) + ' '
            message += str(self.controller.wristRight) + ' '
            message += str(self.controller.gripperClose) + ' '
            message += str(self.controller.gripperOpen) + ' '
            message += str(self.controller.in1) + ' '
            message += str(self.controller.in2) + ' '
            message += str(self.controller.in3) + ' '
            message += str(self.controller.in4) + ' '
            message += str(self.controller.basein1) + ' '
            message += str(self.controller.basein2) + ' '
            message += str(self.controller.elbowin1) + ' '
            message += str(self.controller.elbowin2) + ' '
            message += str(self.controller.wristin1) + ' '
            message += str(self.controller.wristin2) + ' '

        return message

    def run(self):
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket_address = ('192.168.0.11', 8000)
        print('server listening at',socket_address)
        client_socket.connect(socket_address) 
        print("msg send CLIENT CONNECTED TO",socket_address)
        while True:
            if client_socket: 
                while (True):
                    data = self.build()
                    #print(data)
                    send_message(client_socket, data)
                    time.sleep(0.02)



def send_command(controller):
    #controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    message = ControlMessage(controller)
    message.start()
    #message.send_message()
    controller.listen(timeout=60)
    

def send_message(client_socket, data): 
        a = pickle.dumps(data)
        message = struct.pack("Q",len(a))+a
        client_socket.sendall(message)


def video_stream():
    cap = cv2.VideoCapture('http://192.168.0.11:9000/stream.mjpg')
    while(True):
        ret, frame = cap.read()
        frame = cv2.resize(frame, (720,480))
        frame[...,2] = cv2.multiply(frame[...,2], 0.5)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break



#t1 = threading.Thread(target=send_command, args=())
#t2 = threading.Thread(target=video_stream, args=())
#t1.start()
#t2.start()