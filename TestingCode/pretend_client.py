import cv2 
import pyshine as ps
import socket
import pickle
from multiprocessing import Process
HTML="""
        <html>
            <head>
                <title>Video Streaming</title>
            </head>

            <body>
                <center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
            </body>
        </html>
    """

class Main:

    print("Client started...")
    ip_address = '127.0.0.1' # Enter your IP address 
    video_port = 9000 # video port
    cmd_port = 7000 # port for crawler commands

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.ip_address, 6666))

        #test code FIX
        self.video_stream_start()

        p = Process(target=self.server_listener())
        p.start()

    def server_listener(self):
        while True:
            x = self.server.recvfrom(1000000)
            data = x[0]
            data = pickle.loads(data)
            print(data)
        
    def video_stream_start(self):
        try:
            StreamProps = ps.StreamProps
            StreamProps.set_Page(StreamProps,HTML)

            StreamProps.set_Mode(StreamProps,'cv2')
            capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            capture.set(cv2.CAP_PROP_BUFFERSIZE,3)
            capture.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
            capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
            capture.set(cv2.CAP_PROP_EXPOSURE, -3.0)
            capture.set(cv2.CAP_PROP_FPS,120)
            StreamProps.set_Capture(StreamProps,capture)
            StreamProps.set_Quality(StreamProps,90)
            server = ps.Streamer((self.ip_address, self.video_port), StreamProps)
            print('Server started at','http://{}:{}'.format(self.ip_address, self.video_port))
            server.serve_forever()
        except Exception as e:
            print(e)
    
    @staticmethod
    def print_message(x):
        print("Client_Side:{}".format(x))

main = Main()