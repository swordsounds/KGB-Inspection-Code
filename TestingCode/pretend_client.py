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
print("Client started...")
f = open("scrapthis.txt", "w")
f.close()
ip_address = '127.0.0.1' # Enter your IP address 
video_port = 9000 # video port
cmd_port = 7000 # port for crawler commands

def video_stream_start():
    try:
        StreamProps = ps.StreamProps
        StreamProps.set_Page(StreamProps, HTML)
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        capture.set(cv2.CAP_PROP_BUFFERSIZE,3)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
        capture.set(cv2.CAP_PROP_EXPOSURE, -3.0)
        capture.set(cv2.CAP_PROP_FPS,120)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        streamer = ps.Streamer((ip_address, video_port), StreamProps)
        print('Stream started at','http://{}:{}'.format(ip_address, video_port))
        streamer.serve_forever()
    except Exception as e:
        print(e)

def server_listener_start():
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((ip_address, cmd_port))
        f = open("scrapthis.txt", "a")
        while True:
            x = server.recvfrom(1000000)
            data = x[0]
            data = pickle.loads(data)
            f.write(data)

if __name__ == '__main__':
    vid= Process(target=video_stream_start)
    ser= Process(target=server_listener_start)
    vid.start()
    ser.start()