import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
capture.set(cv2.CAP_PROP_FPS,30)
while True:
    ret, frame = capture.read()
    cv2.imshow('Img Server', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break
cv2.destroyAllWindows()