import cv2, pyshine as ps, socket, pickle, csv
from multiprocessing import Process
from subprocess import call
# call("sudo shutdown -h now", shell=True)

SERVER = '127.0.0.1' # Enter your IP address 
VIDPORT = 9000 # video port
CMDPORT = 8000 # port for crawler commands
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

info = {
   'dpad_up': 0,
    'dpad_down': 0,
    'dpad_left': 0,
    'dpad_right': 0,
    'tether': 0,
    'crawl': 0,
    'gripper': 0,
    'arm': 0 
}

def video_stream_start():
    print("Video Client started...")
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
        streamer = ps.Streamer((SERVER, VIDPORT), StreamProps)
        print('Stream started at','http://{}:{}'.format(SERVER, VIDPORT))
        streamer.serve_forever()
    except Exception as e:
        print(e)

def server_listener_start():
        print("Server-Client Connection started...")
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((SERVER, CMDPORT))
        
        fieldnames = ['dpad_up', 'dpad_down', 'dpad_left', 'dpad_right', 'tether', 'crawl','gripper', 'arm']
        
        while True:
            x = server.recvfrom(2048)
            data = x[0]
            data = pickle.loads(data)

            for key, value in data.items():
                 info[key] = value
        
            with open('data.csv', 'w') as csv_file: #test code REMOVE
                csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                csv_writer.writeheader()
                csv_writer.writerow(info)

if __name__ == '__main__':
    vid= Process(target=video_stream_start)
    ser= Process(target=server_listener_start)
    vid.start()
    ser.start()