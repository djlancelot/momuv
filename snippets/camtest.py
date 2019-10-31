import cv2
import numpy as np
#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("rtsp://djlancelot:lacika@192.168.50.145/live")

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

old_frame = None
cnt = 0
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (160,90), interpolation=cv2.INTER_AREA)
    if old_frame is None:
        old_frame = frame
    frameDelta = cv2.absdiff(frame, old_frame)
    cv2.imshow('Input', frame)
    cnt+=1
    if cnt >15:
        cnt=0
        print(np.sum(frameDelta))
        old_frame = frame
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()