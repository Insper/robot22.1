#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        try:
            input_source=int(arg) # se for um device
        except:
            input_source=str(arg) # se for nome de arquivo
    else:   
        input_source = 0

    cap = cv2.VideoCapture(input_source)
    
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            print("Codigo de retorno FALSO - problema para capturar o frame")

        # Our operations on the frame come here
        bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        # cv2.imshow('frame',frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

