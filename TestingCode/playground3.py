import cv2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



while True:
	ret, frame = cap.read()
	frame = cv2.resize(frame, (720,480))
	cv2.imshow('Img Client', frame)



	if cv2.waitKey(5) & 0xFF == 27:
		break
cv2.destroyAllWindows()
cap.release()