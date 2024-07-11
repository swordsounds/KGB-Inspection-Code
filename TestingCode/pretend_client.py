import cv2 
import pyshine as ps


print("Client started...")
def print_message(x):
    print("Client_Side:{}".format(x))

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
StreamProps = ps.StreamProps
StreamProps.set_Page(StreamProps,HTML)

address = ('127.0.0.1',9000) # Enter your IP address 

try:
    StreamProps.set_Mode(StreamProps,'cv2')
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,3)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,2560)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1440)
    capture.set(cv2.CAP_PROP_EXPOSURE, -3.0)
    capture.set(cv2.CAP_PROP_FPS,120)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    server = ps.Streamer(address,StreamProps)
    print('Server started at','http://'+address[0]+':'+str(address[1]))
    server.serve_forever()
except Exception as e:
    print(e)