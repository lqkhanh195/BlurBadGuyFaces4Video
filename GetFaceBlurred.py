import cv2
import numpy as np
import os

src = cv2.VideoCapture("Job Interview_ I Want to Learn (ESL).mp4")
writer = cv2.VideoWriter('temp.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15, (500, 500))

if src.isOpened() == False:
    print("Error opening")

modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "models/deploy.prototxt.txt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

while True: 
    ret, fr = src.read()
    if ret:
        fr = cv2.resize(fr, (500, 500), interpolation=cv2.INTER_AREA)

        h, w = fr.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(fr, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
        net.setInput(blob)
        faces = net.forward()

        x = x1 = y = y1 = 0
        img_face_blurred = fr.copy()
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.3:
                box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x, y, x1, y1) = box.astype("int")

                img_face_blurred[y:y1, x:x1, :] = cv2.blur(img_face_blurred[y:y1, x:x1, :], (75, 75))

        writer.write(img_face_blurred)

    else:
        break

src.release()
writer.release()

src = cv2.VideoCapture("temp.avi")

if src.isOpened() == False:
    print("Error opening")

while True:
    ret, fr = src.read()
    if ret:
        cv2.imshow("Result", fr)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

src.release()

os.remove("temp.avi")