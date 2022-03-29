#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Para funcionar o drone ja ter decolado
    Opere o aparelho via teleop

"""


import rospy
import random
import math

from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry


topico_odom = "/odom"

# Apenas valores para inicializar
x = -1000
y = -1000
z = -1000

def recebeu_leitura(dado):
    """
        Grava nas variáveis x,y,z a posição extraída da odometria
        Atenção: *não coincidem* com o x,y,z locais do drone
    """
    global x
    global y 
    global z 

    x = dado.pose.pose.position.x
    y = dado.pose.pose.position.y
    z = dado.pose.pose.position.z


if __name__=="__main__":

    rospy.init_node("q2")

    # Cria um subscriber que chama recebeu_leitura sempre que houver nova odometria
    recebe_scan = rospy.Subscriber(topico_odom, Odometry , recebeu_leitura)
    
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=3)


    angulo = random.random() * 6.28
    print('Angulo de giro ', math.degrees(angulo))
    vel_ang = math.radians(20)
    vel = Twist(Vector3(0,0,0), Vector3(0,0,vel_ang))
    pub.publish(Twist(Vector3(0, 0, 0), Vector3(0, 0, 0)))
    rospy.sleep(2)
    pub.publish(vel)
    rospy.sleep(angulo/vel_ang)
    pub.publish(Twist(Vector3(0, 0, 0), Vector3(0, 0, 0)))

    try:
        while not rospy.is_shutdown():
            velocidade = Twist(Vector3(0.1, 0, 0), Vector3(0, 0, 0))
            pub.publish(velocidade)
            print("x {} y {} z {}".format(x, y, z))
            distancia = (x*x+y*y)**0.5
            if distancia >= 1.33:
                pub.publish(Twist(Vector3(0, 0, 0), Vector3(0, 0, 0)))
                break
            rospy.sleep(0.1)
    except rospy.ROSInterruptException:
        pub.publish(vel)
        rospy.sleep(1.0)
