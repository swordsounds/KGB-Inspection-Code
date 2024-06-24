# import os
import cv2


filename = 'video.avi'

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    # 'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (1920, 1080))

while True:
    ret, frame = cap.read()
    # print(out.write(frame))
    out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()