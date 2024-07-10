import cv2

cap = cv2.VideoCapture('http://127.0.0.1:9000/stream.mjpg')
while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (720,480))
    # frame[...,2] = cv2.multiply(frame[...,2], 0.5)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break