import cv2
from gaze_tracking import GazeTracking
from datetime import datetime
import numpy as np

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

#motion detection
frameCount = 0
fgbg = cv2.createBackgroundSubtractorMOG2(300, 400, True)

while True:

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #We get a new frame from the webcam
    _, frame = webcam.read()

    frameCount += 1
    # Resize the frame
    resizedFrame = cv2.resize(frame, (0, 0), fx=2, fy=2)
    frame = cv2.resize(frame, (0, 0), fx=1.3, fy=1.3)
    # Get the foreground mask
    fgmask = fgbg.apply(resizedFrame)

    # Count all the non zero pixels within the mask
    count = np.count_nonzero(fgmask)

    print('Frame: %d, Pixel Count: %d' % (frameCount, count))

    # Determine how many pixels do you want to detect to be considered "movement"
    # if (frameCount > 1 and cou`nt > 5000):
    if (frameCount > 1 and count > 5000):
        print('Warning: Do not move')
        cv2.putText(frame, 'Warning: Do not move', (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    #We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) == 0:        
        text = "No FACE FOUND"
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame, text, (50, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking Away"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 0, 255), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 370), cv2.FONT_HERSHEY_DUPLEX, 0.9, (18, 255, 255), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 410), cv2.FONT_HERSHEY_DUPLEX, 0.9, (18, 255, 255), 1)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, str(datetime.now()), (100, 600), font, 1, (18, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Demo", frame)
    cv2.imshow('Mask', fgmask)

    if cv2.waitKey(1) == 10:
        break