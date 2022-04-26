#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
import numpy as np
import math
import cv2
import time
from geometry_msgs.msg import Twist, Vector3, Pose
from sensor_msgs.msg import Image, CompressedImage, LaserScan
from cv_bridge import CvBridge, CvBridgeError


import cv2.aruco as aruco
import sys

#--- Define Tag de teste
id_to_find  = 200
marker_size  = 20 #- [cm]
#id_to_find  = 22
#marker_size  = 3 #- [cm]
# 


#--- Get the camera calibration path
calib_path  = "/home/borg/catkin_ws/src/robot21.2/ros/exemplos/scripts/"
camera_matrix   = np.loadtxt(calib_path+'cameraMatrix_raspi.txt', delimiter=',')
camera_distortion   = np.loadtxt(calib_path+'cameraDistortion_raspi.txt', delimiter=',')

#--- Define the aruco dictionary
aruco_dict  = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
parameters  = aruco.DetectorParameters_create()
parameters.minDistanceToBorder = 0
parameters.adaptiveThreshWinSizeMax = 1000

#-- Font for the text in the image
font = cv2.FONT_HERSHEY_PLAIN

bridge = CvBridge() #converte a msg do ROS para OpenCV
cv_image = None
scan_dist = 0

def scaneou(dado):
	#print("scan")
	global scan_dist 
	scan_dist = dado.ranges[0]*100
	return scan_dist


# A função a seguir é chamada sempre que chega um novo frame
def roda_todo_frame(imagem):
	#print("frame")
	
	try:
		cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8") # imagem compressed
		#cv_image = cv2.flip(cv_image, -1) # Descomente se for robo real
		#cv_image = bridge.imgmsg_to_cv2(imagem, "bgr8") 			# imagem não compressed
		#cv_image = cv2.resize(cv_image,(cv_image.shape[1]*2,cv_image.shape[0]*2)) # resize image se necessario
		
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
		print(ids)


		if ids is not None:
			#-- ret = [rvec, tvec, ?]
			#-- rvec = [[rvec_1], [rvec_2], ...] vetor de rotação
			#-- tvec = [[tvec_1], [tvec_2], ...] vetor de translação
			ret = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)
			rvec, tvec = ret[0][0,0,:], ret[1][0,0,:]

			#-- Desenha um retanculo e exibe Id do marker encontrado
			aruco.drawDetectedMarkers(cv_image, corners, ids) 
			aruco.drawAxis(cv_image, camera_matrix, camera_distortion, rvec, tvec, 1)

			#-- Print tvec vetor de tanslação em x y z
			str_position = "Marker x=%4.0f  y=%4.0f  z=%4.0f"%(tvec[0], tvec[1], tvec[2])
			print(str_position)
			cv2.putText(cv_image, str_position, (0, 100), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

			##############----- Referencia dos Eixos------###########################
			# Linha referencia em X
			cv2.line(cv_image, (cv_image.shape[1]//2,cv_image.shape[0]//2), ((cv_image.shape[1]//2 + 50),(cv_image.shape[0]//2)), (0,0,255), 5) 
			# Linha referencia em Y
			cv2.line(cv_image, (cv_image.shape[1]//2,cv_image.shape[0]//2), (cv_image.shape[1]//2,(cv_image.shape[0]//2 + 50)), (0,255,0), 5) 	
			
			#####################---- Distancia Euclidiana ----#####################
			# Calcula a distancia usando apenas a matriz tvec, matriz de tanslação
			# Pode usar qualquer uma das duas formas
			distance = np.sqrt(tvec[0]**2 + tvec[1]**2 + tvec[2]**2)
			distancenp = np.linalg.norm(tvec)

			#-- Print distance
			str_dist = "Dist aruco=%4.0f  dis.np=%4.0f"%(distance, distancenp)
			print(str_dist)
			cv2.putText(cv_image, str_dist, (0, 15), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

			#####################---- Distancia pelo foco ----#####################
			#https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
			
			# raspicam v2 focal legth 
			FOCAL_LENGTH = 3.6 #3.04
        	# pixel por unidade de medida
			m = (camera_matrix[0][0]/FOCAL_LENGTH + camera_matrix[1][1]/FOCAL_LENGTH)/2
			# corners[0][0][0][0] = [ID][plano?][pos_corner(sentido horario)][0=valor_pos_x, 1=valor_pos_y]	
			pixel_length1 = math.sqrt(math.pow(corners[0][0][0][0] - corners[0][0][1][0], 2) + math.pow(corners[0][0][0][1] - corners[0][0][1][1], 2))
			pixel_length2 = math.sqrt(math.pow(corners[0][0][2][0] - corners[0][0][3][0], 2) + math.pow(corners[0][0][2][1] - corners[0][0][3][1], 2))
			pixlength = (pixel_length1+pixel_length2)/2
			dist = marker_size * FOCAL_LENGTH / (pixlength/m)
			
			#-- Print distancia focal
			str_distfocal = "Dist focal=%4.0f"%(dist)
			print(str_distfocal)
			cv2.putText(cv_image, str_distfocal, (0, 30), font, 1, (0, 255, 0), 1, cv2.LINE_AA)	


			####################--------- desenha o cubo -----------#########################
			# https://github.com/RaviJoshii/3DModeler/blob/eb7ca48fa06ca85fcf5c5ec9dc4b562ce9a22a76/opencv/program/detect.py			
			m = marker_size/2
			pts = np.float32([[-m,m,m], [-m,-m,m], [m,-m,m], [m,m,m],[-m,m,0], [-m,-m,0], [m,-m,0], [m,m,0]])
			imgpts, _ = cv2.projectPoints(pts, rvec, tvec, camera_matrix, camera_distortion)
			imgpts = np.int32(imgpts).reshape(-1,2)
			cv_image = cv2.drawContours(cv_image, [imgpts[:4]],-1,(0,0,255),4)
			for i,j in zip(range(4),range(4,8)): cv_image = cv2.line(cv_image, tuple(imgpts[i]), tuple(imgpts[j]),(0,0,255),4);
			cv_image = cv2.drawContours(cv_image, [imgpts[4:]],-1,(0,0,255),4)
			

		# Exibe tela
		cv2.imshow("Camera", cv_image)
		cv2.waitKey(1)
	except CvBridgeError as e:
		print('ex', e)
	
if __name__=="__main__":
	rospy.init_node("aruco")

	topico_imagem = "/camera/image/compressed" #robo simulado
	#topico_imagem = "/raspicam/image_raw/compressed" #robo real
	recebe_imagem = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)

	# Teste com imagem não compressed
	#topico_imagem = "/camera/image"
	#recebe_imagem = rospy.Subscriber(topico_imagem, Image, roda_todo_frame, queue_size=4, buff_size = 2**24)
	
	print("Usando ", topico_imagem)

	# validação da distância usando laser scan
	#recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
	
	
	try:

		while not rospy.is_shutdown():
			rospy.sleep(0.1)

	except rospy.ROSInterruptException:
	    print("Ocorreu uma exceção com o rospy")
