import cv2
import pyshine as ps
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
StreamProps = ps.StreamProps
StreamProps.set_Page(StreamProps,HTML)

address = ('127.0.0.1',9000) # Enter your IP address 

try:
    StreamProps.set_Mode(StreamProps,'cv2')
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_BUFFERSIZE,3)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    capture.set(cv2.CAP_PROP_FPS,60)
    StreamProps.set_Capture(StreamProps,capture)
    StreamProps.set_Quality(StreamProps,90)
    server = ps.Streamer(address,StreamProps)
    print('Server started at','http://'+address[0]+':'+str(address[1]))
    server.serve_forever()
except Exception as e:
    print(e)

