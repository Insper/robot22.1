from __future__ import with_statement
import cv2 as cv
import numpy as np

with open("coco-labels","r") as f:
        class_names = f.readlines()

cvNet = cv.dnn.readNetFromDarknet('yolov4-csp-x-swish.cfg', 'yolov4-csp-x-swish.weights')
model = cv.dnn_DetectionModel(cvNet)
model.setInputParams(size=(640, 640), scale=1/255, swapRB=True)

img = cv.imread('cat_bike.png')

cap = cv.VideoCapture(0)
ret = True

while ret:
        ret, img = cap.read()

        classes, scores, boxes = model.detect(img, 0.4, 0.2)

        for (classid, score, box) in zip(classes, scores, boxes):
                color = (213, 42, 214)
                label = "%s : %f" % (class_names[classid[0]], score)
                cv.rectangle(img, box, color, 2)
                cv.putText(img, label, (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)        

        cv.imshow('img', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
	        break

cv.destroyAllWindows()