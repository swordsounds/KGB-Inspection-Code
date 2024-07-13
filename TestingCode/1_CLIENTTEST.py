import socket, pickle
from multiprocessing import Process
import cv2, pyshine as ps

HEADER = 2048
CMDPORT = 8000
VIDPORT = 9000
FORMAT = 'utf-8'
DC_MESSAGE = "!DISCONNECT"
SERVER = "192.168.0.23"
ADDR = (SERVER, CMDPORT)
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b" " * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))

def video_stream_start():
    try:
        StreamProps = ps.StreamProps
        StreamProps.set_Page(StreamProps, HTML)
        StreamProps.set_Mode(StreamProps,'cv2')
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        capture.set(cv2.CAP_PROP_BUFFERSIZE,3)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        capture.set(cv2.CAP_PROP_EXPOSURE, -4.0)
        capture.set(cv2.CAP_PROP_FPS,30)
        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        streamer = ps.Streamer((SERVER, VIDPORT), StreamProps)
        print('Stream started at','http://{}:{}'.format(SERVER, VIDPORT))
        streamer.serve_forever()
    except Exception as e:
        print(e)


def server_listener_start():
        print("Client Listening...")
        while True:
            x = client.recvfrom(2048)
            data = x[0]
            data = pickle.loads(data)

            with open("scrapthis.txt", "w", newline='\n') as f: #test code REMOVE
                 f.write(f'{data}')
            f.close()

if __name__ == '__main__':
    vid= Process(target=video_stream_start)
    ser= Process(target=server_listener_start)
    vid.start()
    ser.start()
    send(DC_MESSAGE)