import cv2
import numpy as np
import os, sys
import tensorflow as tf
from math import *

modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "models/deploy.prototxt.txt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

still_blurring = True

def build_model():
    inputs = tf.keras.layers.Input((224,224,3),name = 'input')

    model = tf.keras.applications.EfficientNetV2B0(include_top=False, weights="imagenet",input_tensor = inputs)
    x = model.output
    x = tf.keras.layers.GlobalAveragePooling2D(name = 'pooling')(x)
    outputs = tf.keras.layers.Dense(1,activation = 'sigmoid',name = 'outputs')(x)

    model = tf.keras.Model(inputs=inputs , outputs =outputs)

    return model

def freeze_model_layers(model):
    l = len(model.layers)
    for i,layer in enumerate(model.layers):
        if i > 0.7* l:
            break
        layer.trainable = False

    return model

model = build_model()
model = freeze_model_layers(model)
model.load_weights("models/model_weight.h5")

def pixelate_image(image, grid_size):
	(h, w) = image.shape[:2]
	xGridLines = np.linspace(0, w, grid_size + 1, dtype="int")
	yGridLines = np.linspace(0, h, grid_size + 1, dtype="int")

	for i in range(1, len(xGridLines)):
		for j in range(1, len(yGridLines)):
                        
			cell_startX = xGridLines[j - 1]
			cell_startY = yGridLines[i - 1]
			cell_endX = xGridLines[j]
			cell_endY = yGridLines[i]

			cell = image[cell_startY:cell_endY, cell_startX:cell_endX]

			(B, G, R) = [int(x) for x in cv2.mean(cell)[:3]]
			cv2.rectangle(image, (cell_startX, cell_startY), (cell_endX, cell_endY),
				(B, G, R), -1)

	return image

def blurVid(path):
    global still_blurring
    still_blurring = True

    src = cv2.VideoCapture(path)
    vid_width  = int(src.get(3))
    vid_height = int(src.get(4))
    print((vid_width,vid_height))
    writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (vid_width, vid_height))

    if src.isOpened() == False:
        print("fail")
        return False
    
    while still_blurring: 
        ret, fr = src.read()
        if ret:
            # fr = cv2.resize(fr, (500, 500), interpolation=cv2.INTER_AREA)

            h, w = fr.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(fr, (300, 300)), 1.0, (300, 300), (104.0, 117.0, 123.0))
            net.setInput(blob)
            faces = net.forward()

            x = x1 = y = y1 = 0
            face_blurred = fr.copy()
            for i in range(faces.shape[2]):
                confidence = faces[0, 0, i, 2]
                if confidence > 0.3:
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x, y, x1, y1) = box.astype("int")

                    face_to_pred = face_blurred[y:y1, x:x1, :].copy()
                    face_to_pred = cv2.resize(face_to_pred, (224, 224), interpolation = cv2.INTER_AREA)
                    pred = model.predict(face_to_pred.reshape(1,224,224,3))
                    pred = np.where(pred > 0.5, 1,0)
                    if pred[0][0] == 1:                   
                        face_blurred[y:y1, x:x1, :] = pixelate_image(face_blurred[y:y1, x:x1, :], grid_size=int(w * 0.01))

            writer.write(face_blurred)
        else:
            print("Done")
            break


    src.release()
    writer.release()

def saveVid(new_name):
    if os.path.exists("output.mp4"):
        os.rename("output.mp4", new_name)

def deleteVid():
    if os.path.exists("output.mp4"):
        os.remove("output.mp4")