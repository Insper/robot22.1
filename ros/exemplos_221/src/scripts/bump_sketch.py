#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
import numpy as np
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import UInt8

bumper = 0

def colidiu(dado):
	global bumper
	bumper = dado.data
	print(dado.data)


if __name__=="__main__":

	rospy.init_node("")

	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
	recebe_scan = rospy.Subscriber("/bumper", UInt8, colidiu)

    v = 0.3
    w = 0.1

	while not rospy.is_shutdown():
        print("Leitura do bumper ", bumper)
		velocidade = Twist(Vector3(v, 0, 0), Vector3(0, 0,w))
		velocidade_saida.publish(velocidade)
		rospy.sleep(0.5)
