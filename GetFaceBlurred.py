import cv2
import numpy as np

src = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

if src.isOpened() == False:
    print("Error opening")

while True: 
    ret, fr = src.read()
    if ret == True:
        fr = cv2.resize(fr, (500, 500), interpolation=cv2.INTER_AREA)
        fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        face = cascade.detectMultiScale(fr, scaleFactor=1.25, minNeighbors=1, minSize=(0, 0))
        for (x, y, w, h) in face:
            cv2.rectangle(fr, (x, y), (x + w, y + h), (0, 255, 0), 4)
        print(face)

        # blur = cv2.blur(fr, (75, 75))

        # cv2.imshow("blurred", blur)
        cv2.imshow("test", fr)

        key = cv2.waitKey(10)
        if key == 27:
            break