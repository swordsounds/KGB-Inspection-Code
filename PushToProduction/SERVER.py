import cv2, socket, pickle, csv, os # type: ignore
from gpiozero import Robot, Motor # type: ignore
from multiprocessing import Process
from subprocess import call
from libcamera import controls # type: ignore
from picamera2 import Picamera2 # type: ignore
from http import server
import socketserver
import logging
from Focuser import Focuser # type: ignore
from Autofocus import AutoFocus # type: ignore

# call("sudo shutdown -h now", shell=True)

SERVER = '192.168.0.19' # Enter your IP address 
VIDPORT_0 = 9000 # video port
VIDPORT_1 = 9100 # video port
VIDPORT_2 = 9200 # video port
VIDPORT_3 = 9300 # video port
CMDPORT = 8000 # port for crawler commands

FOCUSER = Focuser(1)

FOCUSER.set(Focuser.OPT_FOCUS, 16000)
FOCUSER.set(Focuser.OPT_ZOOM, 3000)
FOCUSER.set(Focuser.OPT_MOTOR_X, 0)

info = {
    'TETH': '', 
    'CRAWL': '',
    'GRIP': '', 
    'ARM': '',
    'ARDU_CAMERA': '', 
    'IR_CUT': '',
    'PTZ_ZOOM': '', 
    'PTZ_FOCUS': '', 
    'PTZ_MOVEMENT': ''
}

capture_0 = cv2.VideoCapture(0)
capture_0.set(cv2.CAP_PROP_FRAME_WIDTH,320)
capture_0.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
capture_0.set(cv2.CAP_PROP_EXPOSURE, -18) 
capture_0.set(cv2.CAP_PROP_BUFFERSIZE,4)
capture_0.set(cv2.CAP_PROP_FPS,30)

capture_1 = cv2.VideoCapture(2)
capture_1.set(cv2.CAP_PROP_FRAME_WIDTH,320)
capture_1.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
capture_1.set(cv2.CAP_PROP_EXPOSURE, -18) 
capture_1.set(cv2.CAP_PROP_BUFFERSIZE,4)
capture_1.set(cv2.CAP_PROP_FPS,30)

class Streamer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
class StreamProps(server.BaseHTTPRequestHandler):
    def set_Capture(self,capture):
        self.capture = capture
    def set_Mode(self,mode):
        self.mode = mode
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            if self.mode == 'cv2':
                try:
                    while True:
                        ret,img = self.capture.read()
                        frame = cv2.imencode('.JPEG', img,[cv2.IMWRITE_JPEG_QUALITY,70])[1].tobytes()
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
                    
            if self.mode == 'picamera2':
                try:
                    while True:
                        img = self.capture.capture_array()
                        frame = cv2.imencode('.JPEG', img, [cv2.IMWRITE_JPEG_QUALITY, 85])[1].tobytes()
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
        '''
        DEFINE ALL SERVOS, MOTORS, ETC IN ACCOCIATED PROCESS

        Breaks whenever you dont. I have no idea why I'll just accept it.

        '''
        
        ROBOT = Robot(right=Motor(19, 13), left=Motor(18, 12))

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((SERVER, CMDPORT))
        
        fieldnames = ['TETH', 'CRAWL','GRIP', 'ARM',
                      'ARDU_CAMERA', 'IR_CUT',
                      'PTZ_ZOOM', 'PTZ_FOCUS', 'PTZ_MOVEMENT']
        try:
            while True:
                x = server.recvfrom(2048)
                data = x[0]
                data = pickle.loads(data)
            
                for key, value in data.items():
                    info[key] = value           
            
                with open('data.csv', 'w') as csv_file: #test code REMOVE
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)#test code REMOVE
                    csv_writer.writeheader()#test code REMOVE
                    csv_writer.writerow(info)#test code REMOVE        



                if info['CRAWL'] == 'FORW':
                    ROBOT.forward(speed=0.5)
                if info['CRAWL'] == 'RIGHT':
                    ROBOT.right(speed=0.5) 
                if info['CRAWL'] == 'BACK':
                    ROBOT.backward(speed=0.5)
                if info['CRAWL'] == 'LEFT':
                    ROBOT.left(speed=0.5)
                if info['CRAWL'] == '':
                    ROBOT.stop()

                if info['ARM'] == 'EXT':
                    pass
                if info['ARM'] == 'RETR':
                    pass



                if info['GRIP'] == 'OPEN':
                    pass
                if info['GRIP'] == 'CLOSE':
                    pass
                if info['GRIP'] == 'RIGHT':
                    pass
                if info['GRIP'] == 'LEFT':
                    pass



                if info['TETH'] == 'EXT':
                    pass
                if info['TETH'] == 'RETR':
                    pass
                if info['TETH'] == 'STOP':
                    pass



                if info['PTZ_FOCUS'] == 'AUTO':
                    autoFocus = AutoFocus(FOCUSER, 'http://192.168.0.19:9100/stream.mjpg')
                    autoFocus.debug = False
                    autoFocus.startFocus()
                if info['PTZ_FOCUS'].split('_')[0] == 'ON':
                    FOCUSER.set(Focuser.OPT_FOCUS, int(info['PTZ_FOCUS'].split('_')[1]))
                if info['PTZ_FOCUS'] == '+':
                    FOCUSER.set(Focuser.OPT_FOCUS,FOCUSER.get(Focuser.OPT_FOCUS) + 100)
                if info['PTZ_FOCUS'] == '-':
                    FOCUSER.set(Focuser.OPT_FOCUS,FOCUSER.get(Focuser.OPT_FOCUS) - 100)



                if info['PTZ_ZOOM'].split('_')[0] == 'ON':
                    FOCUSER.set(Focuser.OPT_ZOOM, int(info['PTZ_ZOOM'].split('_')[1]))
                if info['PTZ_ZOOM'] == '+':
                    FOCUSER.set(Focuser.OPT_ZOOM,FOCUSER.get(Focuser.OPT_ZOOM) + 1000)
                if info['PTZ_ZOOM'] == '-':
                    FOCUSER.set(Focuser.OPT_ZOOM,FOCUSER.get(Focuser.OPT_ZOOM) -1000)



                if info['PTZ_MOVEMENT'] == 'UP':
                    pass
                if info['PTZ_MOVEMENT'] == 'RIGHT':
                    FOCUSER.set(Focuser.OPT_MOTOR_X, FOCUSER.get(Focuser.OPT_MOTOR_X) + 1)
                if info['PTZ_MOVEMENT'] == 'DOWN':
                    pass
                if info['PTZ_MOVEMENT'] == 'LEFT':
                    FOCUSER.set(Focuser.OPT_MOTOR_X, FOCUSER.get(Focuser.OPT_MOTOR_X) - 1)



                if info['IR_CUT'] == 'True':
                    FOCUSER.set(Focuser.OPT_IRCUT,FOCUSER.get(Focuser.OPT_IRCUT)^0x0001)



                if info['ARDU_CAMERA'] == 'ONE':
                    os.system('i2cset -y 6 0x24 0x24 0x02')
                if info['ARDU_CAMERA'] == 'TWO':
                    os.system('i2cset -y 6 0x24 0x24 0x12')
                if info['ARDU_CAMERA'] == 'THREE':
                    os.system('i2cset -y 6 0x24 0x24 0x22')
                if info['ARDU_CAMERA'] == 'FOUR':
                    os.system('i2cset -y 6 0x24 0x24 0x32')
                if info['ARDU_CAMERA'] == 'RESET':
                    os.system('i2cset -y 6 0x24 0x24 0x00')
                            
        except Exception as e:
            print(e)

def video_0_start():
    ardu_cam = Picamera2(0)
    ardu_cam.preview_configuration.main.size=(1280,720) #full screen : 3280 2464, 1920x1080 for 1, 2464x1736 for 0
    ardu_cam.preview_configuration.main.format = "RGB888" #8 bits
    ardu_cam.preview_configuration.raw.format = 'SRGGB8'
    ardu_cam.set_controls({"FrameDurationLimits": (40000, 40000)})
    ardu_cam.start()

    vid0 = StreamProps
    vid0.set_Mode(StreamProps, 'picamera2')
    vid0.set_Capture(StreamProps, ardu_cam)
    vid_stream_0 = Streamer((SERVER, VIDPORT_0), vid0)
    print('Stream started at','http://{}:{}/stream.mjpg'.format(SERVER, VIDPORT_0))
    ardu_cam.set_controls({"AfMode":controls.AfModeEnum.Continuous})

    vid_stream_0.serve_forever()

def video_1_start():
    ptz_cam = Picamera2(1)
    ptz_cam.preview_configuration.main.size=(1280,720) #full screen : 3280 2464, 1920x1080 for 1, 2464x1736 for 0
    ptz_cam.preview_configuration.main.format = "RGB888" #8 bits
    ptz_cam.preview_configuration.raw.format = 'SRGGB8'
    ptz_cam.set_controls({"FrameDurationLimits": (40000, 40000)})
    ptz_cam.start()

    vid1 = StreamProps
    vid1.set_Mode(StreamProps, 'picamera2')
    vid1.set_Capture(StreamProps, ptz_cam)
    vid_stream_1 = Streamer((SERVER, VIDPORT_1), vid1)
    print('Stream started at','http://{}:{}/stream.mjpg'.format(SERVER, VIDPORT_1))

    vid_stream_1.serve_forever()

def video_2_start():
    vid2 = StreamProps
    vid2.set_Mode(StreamProps, 'cv2')
    vid2.set_Capture(StreamProps, capture_0)
    vid_stream_2 = Streamer((SERVER, VIDPORT_2), vid2)
    print('Stream started at','http://{}:{}/stream.mjpg'.format(SERVER, VIDPORT_2))

    vid_stream_2.serve_forever()

def video_3_start():
    vid3 = StreamProps
    vid3.set_Mode(StreamProps, 'cv2')
    vid3.set_Capture(StreamProps, capture_1)
    vid_stream_3 = Streamer((SERVER, VIDPORT_3), vid3)
    print('Stream started at','http://{}:{}/stream.mjpg'.format(SERVER, VIDPORT_3))

    vid_stream_3.serve_forever()

if __name__ == '__main__':
    try:
        ser = Process(target=server_listener_start)
        vid_0_str = Process(target=video_0_start)
        vid_1_str = Process(target=video_1_start)
        vid_2_str = Process(target=video_2_start)
        vid_3_str = Process(target=video_3_start)
        ser.start()
        vid_0_str.start()
        vid_1_str.start()
        vid_2_str.start()
        vid_3_str.start()
        

    except Exception as e:
        print(e)