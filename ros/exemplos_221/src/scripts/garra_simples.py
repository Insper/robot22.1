#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Float64

if __name__ == "__main__":
    rospy.init_node("garra")
    ombro = rospy.Publisher("/joint1_position_controller/command", Float64, queue_size=1)
    garra = rospy.Publisher("/joint2_position_controller/command", Float64, queue_size=1)

    try:
        while not rospy.is_shutdown():
            ombro.publish(-1.0) ## para baixo
            garra.publish(0.0)  ## Fechado
            rospy.sleep(3.0)
            ombro.publish(1.5) ## para cima
            garra.publish(-1.0) ## Aberto
            rospy.sleep(3.0)
            ombro.publish(0.0) ## para frente

    except rospy.ROSInterruptException:
        print("Ocorreu uma exceção com o rospy")
