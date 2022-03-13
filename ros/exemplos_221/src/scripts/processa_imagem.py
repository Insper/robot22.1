#! /usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = ["Rachel P. B. Moraes", "Igor Montagner", "Fabio Miranda"]


import rospy
import numpy as np
import tf
import math
import cv2
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import cormodule

bridge = CvBridge()

cv_image = None
atraso = 1.5E9  # 1 segundo e meio. Em nanossegundos

# Só usar se os relógios ROS da Raspberry e do Linux desktop estiverem sincronizados.
# Descarta imagens que chegam atrasadas demais
check_delay = False

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
    topico_imagem = "camera/rgb/image_raw/compressed" # Use para robo virtual
    
    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)
    print("Usando ", topico_imagem)

    try:

        while not rospy.is_shutdown():
            
            antes = rospy.Time.now() 
            if cv_image is not None:
                
                media, centro, maior_area =  cormodule.identifica_cor(cv_image)
                cv2.imshow("Camera", cv_image)

            depois = rospy.Time.now()
            duration = (depois - antes).to_sec()

            print(f'O processamento levou {duration} s')

            rospy.sleep(0.033 - duration)

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
