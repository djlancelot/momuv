import cv2
import numpy as np
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

old_frame = None
cnt = 0
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    if old_frame is None:
        old_frame = frame
    frameDelta = cv2.absdiff(frame, old_frame)
    cv2.imshow('Input', frameDelta)
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