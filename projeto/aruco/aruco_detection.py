#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import cv2.aruco as aruco
import numpy as np 
import sys 

if __name__ == "__main__":
    if len(sys.argv) > 1:
       arg = sys.argv[1]
       try:
           input_source=int(arg) # se for um device
       except:
           input_source=str(arg) # se for nome de arquivo
    else:   
       input_source = "aruco.mp4"

    print("Baixe o arquivo a seguir para funcionar: ")
    print("https://github.com/Insper/robot202/raw/master/projeto/aruco/aruco.mp4")

    cap = cv2.VideoCapture(input_source)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            print("Codigo de retorno FALSO - problema para capturar o frame")

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #--- Define the aruco dictionary
        aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
        # parameters  = aruco.DetectorParameters_create()
        # parameters.minDistanceToBorder = 0
        # parameters.adaptiveThreshWinSizeMax = 1000

        try:
            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict) #, parameters=parameters)

            for i in range(len(ids)):
                print('ID: {}'.format(ids[i]))
                
                for c in corners[i]: 
                    for canto in c:
                        print("Corner {}".format(canto))




            aruco.drawDetectedMarkers(frame, corners, ids)
        
        except:
            print("No aruco detected...")


        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

