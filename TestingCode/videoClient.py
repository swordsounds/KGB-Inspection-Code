# # import cv2 
# import socket
# import pickle

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

# server_ip = '127.0.0.1'
# server_port = 6666

# # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# # cap.set(3, 640)
# # cap.set(4, 480)

# while True:
#     buffer="hello world"
#     x_as_bytes = pickle.dumps(buffer)

#     s.sendto((x_as_bytes), (server_ip, server_port))
# while cap.isOpened():

#     ret, img = cap.read()

#     cv2.imshow('Img Client', img)

#     ret, buffer = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    # x_as_bytes = pickle.dumps(buffer)

    # s.sendto((x_as_bytes), (server_ip, server_port))

#     if cv2.waitKey(5) & 0xFF == 27:
#         break
# cv2.destroyAllWindows()
# cap.release()

import cv2 
  
  
# define a video capture object 
# vid = cv2.VideoCapture('http://192.168.0.19:9000/') 

# while vid.isOpened(): 
      
#     # Capture the video frame 
#     # by frame 
#     ret, frame = vid.read() 
  
#     # Display the resulting frame 
#     cv2.imshow('frame', frame) 
      
#     # the 'q' button is set as the 
#     # quitting button you may use any 
#     # desired button of your choice 
#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         break
  
# # After the loop release the cap object 
# vid.release() 
# # Destroy all the windows 
# cv2.destroyAllWindows() 
from http import server
import socketserver
import logging

class Streamer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    
class StreamProps(server.BaseHTTPRequestHandler):

    def set_Page(self,PAGE):
        self.PAGE = PAGE
    def set_Capture(self,capture):
        self.capture = capture
    def set_Quality(self,quality):
        self.quality = quality
    def set_Mode(self,mode):
        self.mode = mode
    def set_Output(self,output):
        self.output = output
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = self.PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            if self.mode == 'cv2':
                try:
                    while True:
                        rc,img = self.capture.read()
                        
                        frame = cv2.imencode('.JPEG', img,[cv2.IMWRITE_JPEG_QUALITY,self.quality])[1].tobytes()
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