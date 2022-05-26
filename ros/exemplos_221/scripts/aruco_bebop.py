#! /usr/bin/env python3
# -*- coding:utf-8 -*-


import cv2
import cv2.aruco as aruco
import numpy as np 
import sys 

import rospy
import numpy as np
import tf
import math
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cormodule

__author__ = ["Rachel P. B. Moraes", "Igor Montagner", "Fabio Miranda"]

bridge = CvBridge()

cv_image = None
atraso = 1.5E9  # 1 segundo e meio. Em nanossegundos

# Só usar se os relógios ROS da Raspberry e do Linux desktop estiverem sincronizados.
# Descarta imagens que chegam atrasadas demais
check_delay = True

# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
    ''' Função chamada sempre que chega um novo frame, e retorna a imagem do OpenCV '''

    print("frame")
    global cv_image
    now = rospy.get_rostime()
    imgtime = imagem.header.stamp
    lag = now-imgtime  # calcula o lag
    delay = lag.nsecs
    print("delay ", "{:.3f}".format(delay/1.0E9))
    if delay > atraso and check_delay == True:
        print("Descartando por causa do delay do frame:", delay)
        return
    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        # cv_image = cv2.flip(cv_image, -1) # Descomente se for robo real
    except CvBridgeError as e:	print('ex', e)
    
if __name__=="__main__":
    rospy.init_node("processa_imagem")

    # topico_imagem = "/kamera"
    topico_imagem = "/bebop/image_raw/compressed" # Use para robo virtual
    
    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
    print("Usando ", topico_imagem)

    try:

        while not rospy.is_shutdown():
            
            antes = rospy.Time.now() 
            if cv_image is not None:
                frame = cv_image
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


            depois = rospy.Time.now()
            duration = (depois - antes).to_sec()

            print(f'O processamento levou {duration} s')
            rospy.sleep(0.033 - duration)
                

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
