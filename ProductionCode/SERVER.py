import cv2, pyshine as ps, socket, pickle, csv
from multiprocessing import Process
from subprocess import call
from picamera2 import Picamera2
from http import server
import socketserver
import logging

# call("sudo shutdown -h now", shell=True)

SERVER = '192.168.0.19' # Enter your IP address 
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

# capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

picam2 = Picamera2()
video_config = picam2.create_video_configuration({'format': 'RGB888'})
picam2.configure(video_config)
picam2.start()

class Streamer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
class StreamProps(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    img = picam2.capture_array()
                    frame = cv2.imencode('.JPEG', img, [cv2.IMWRITE_JPEG_QUALITY, 100000000])[1].tobytes()
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

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
    print("Video Client started...")
    try:
        ser= Process(target=server_listener_start)
        ser.start()

        streamer = Streamer((SERVER, VIDPORT), StreamProps)
        print('Stream started at','http://{}:{}/stream.mjpg'.format(SERVER, VIDPORT))
        streamer.serve_forever()
    except Exception as e:
        print(e)
    