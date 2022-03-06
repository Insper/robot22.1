#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2

print("Baixe o arquivo a seguir para funcionar: ")
print("https://github.com/Insper/robot20/raw/master/aula02/hall_box_battery_1024.mp4")

cap = cv2.VideoCapture('hall_box_battery_1024.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")

    # Our operations on the frame come here
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    # cv2.imshow('frame',frame)
    cv2.imshow('gray', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

