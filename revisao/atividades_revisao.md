
# Atividades de revisão

Lembre-se de que também existem [as provas e simulados anteriores](./lista_provas_anteriores.md).

# 1. Revisão para a P1

[Código do simulado da prova](https://github.com/insper-classroom/221_robot_sim1)

[Gabarito do simulado](https://github.com/insper-classroom/221_robot_sim1/tree/gabarito)


# 2. Revisão de ROS feita para a P1 do semestre passado

[Código do simulado da prova](https://github.com/insper-classroom/211_robot_sim)

[Gabarito do simulado](https://github.com/insper-classroom/211_robot_sim)

[Aula de terça](https://web.microsoftstream.com/video/451bee6e-ad81-456a-b338-28c5895e0e80)

[Aula de quinta](https://web.microsoftstream.com/video/e734cfa2-2a79-41bb-a265-f260673cbc8e)


# 3. Revisão de OpenCV 

[Vídeo da revisão](https://web.microsoftstream.com/video/0f2663ed-7258-42f5-8d9b-6db04ba55431)


[O código da revisão se encontra aqui](https://github.com/mirwox/revisao2020/blob/master/Revisao_Imagem.ipynb)



# 4. Revisão de ROS


Enunciado:

[https://github.com/Insper/r2019_delta/blob/master/enunciado.md](https://github.com/Insper/r2019_delta/blob/master/enunciado.md)


## Vídeo com desenvolvimento das soluções

[https://web.microsoftstream.com/video/2f7b8fec-add8-4300-b902-2daf40fd4676?list=studio](https://web.microsoftstream.com/video/2f7b8fec-add8-4300-b902-2daf40fd4676)


## 4.1 Questão de Twist e Odometria

Faça um programa em ROS que realize as seguintes tarefas:

* Sorteia um ângulo $\alpha$

* Gira o robô uma magnitude $\alpha$ no sentido horário

* Faz o robô comećar a andar em frente (em suas coordenadas locais)

* Usa a odometria (tópico `\odom`) para deixar o robô imóvel depois que este andou $1.33m$ em relaćão a sua posićào inicial

|Resultado| Conceito| 
|---|---|
| Não executa | 0 |
| Gira alpha no sentido certo | 1.0 |
|  Recebe odometria | 1.5 |
| Para após andar | 2.5 | 


## 4.2 Resposta da Q3 



Código de gabarito:

[https://github.com/Insper/r2019_delta/blob/revisao-jun-2020/p1_delta/scripts/gab_q3.py](https://github.com/Insper/r2019_delta/blob/revisao-jun-2020/p1_delta/scripts/gab_q3.py)

```python
#! /usr/bin/env python
# -*- coding:utf-8 -*-

# Sugerimos rodar com:
# roslaunch turtlebot3_gazebo  turtlebot3_empty_world.launch 


from __future__ import print_function, division
import rospy
import numpy as np
import cv2
from geometry_msgs.msg import Twist, Vector3
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Vector3
import math
import time
from tf import transformations
import sys


def dist(x1,y1, x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)



x = None
y = None

contador = 0
pula = 50

def recebe_odometria(data):
    global x
    global y
    global contador

    x = data.pose.pose.position.x
    y = data.pose.pose.position.y

    quat = data.pose.pose.orientation
    lista = [quat.x, quat.y, quat.z, quat.w]
    angulos = np.degrees(transformations.euler_from_quaternion(lista))    

    if contador % pula == 0:
        print("Posicao (x,y)  ({:.2f} , {:.2f}) + angulo {:.2f}".format(x, y,angulos[2]))
    contador = contador + 1



if __name__=="__main__":

    rospy.init_node("exemplo_odom")

    t0 = rospy.get_rostime()


    pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )

    ref_odometria = rospy.Subscriber("/odom", Odometry, recebe_odometria)

    # Variaveis da solucao
    import random

    w = 0.3

    zero = Twist(Vector3(0,0,0), Vector3(0,0,0))

    while not rospy.is_shutdown():
        rospy.sleep(1.0)  # sleep para contornar bugs
        # Resposta comeca abaixo

        # sorteia angulo

        alfa = random.uniform(0, 2*math.pi)
        t_rot = alfa/w
        print("Alfa: {} Tempo: {}".format(alfa, t_rot))

        # girar aquele angulo no sentido horario
        vel_rot = Twist(Vector3(0,0,0), Vector3(0,0,-w))
        pub.publish(vel_rot)
        rospy.sleep(t_rot)
        # Acbou o tempo da rotacao
        pub.publish(zero)
        rospy.sleep(0.5)

        x0 = x
        y0 = y
        finished = False
        vel_trans = Twist(Vector3(0.2,0,0), Vector3(0,0,0))

        while not finished:
            pub.publish(vel_trans)
            rospy.sleep(0.05)
            if dist(x0, y0, x, y) >= 1.33:
                finished = True
    

        pub.publish(zero)

        # baseado na odometria, parar depois de andar 1.33m
        print("terminou")
        rospy.sleep(0.5)
        sys.exit(0)

```




# Questão 4 - ROS + cv

**Atenćão: você vai usar OpenCV mas não vai trabalhar com imagens de câmera**

Você deve trabalhar no arquivo `le_scan_grafico.py`

O que você deve fazer:
* Leia os dados do *lidar* 
* Represente o robô na coordenada 256,256 da imagem usando um círculo
* Adotando a escala $1 pixel = 2 cm$ desenhe todas as leituras válidas do lidar na imagem
* Traça as retas encontradas usando a transformada de Hough Lines


|Resultado| Conceito| 
|---|---|
| Não executa | 0 |
| Desenha os pontos corretamente | 1.5 |
|  Traça a reta | 2.5 | 


## Gabarito online

Resposta online:

[https://github.com/Insper/r2019_delta/blob/revisao-jun-2020/p1_delta/scripts/le_scan_grafico.py](https://github.com/Insper/r2019_delta/blob/revisao-jun-2020/p1_delta/scripts/le_scan_grafico.py)

## Código da resposta: 

```python
#! /usr/bin/env python
# -*- coding:utf-8 -*-

import rospy

import numpy as np

import cv2

import math

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

laser = None

def scaneou(dado):
    print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    print("Leituras:")
    atual = np.array(dado.ranges).round(decimals=2)
    print(atual)
    global laser
    laser = atual.copy()
    #print("Intensities")
    #print(np.array(dado.intensities).round(decimals=2))


def desenha(cv_image):
    """
        Use esta funćão como exemplo de como desenhar na tela
    """
    #cv2.circle(cv_image,(256,256),64,(0,255,0),2)
    #cv2.line(cv_image,(256,256),(400,400),(255,0,0),5)
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(cv_image,'Boa sorte!',(0,50), font, 2,(255,255,255),2,cv2.LINE_AA)

    img = cv_image 

    if laser is not None:
        for  i in range(len(laser)):
            alpha = math.radians(i)
            cx, cy = (256, 256)
            d = laser[i]
            if 0.12  < d < 3.5:
                px = cx - d*math.sin(alpha)*50
                py = cy - d*math.cos(alpha)*50
                cv2.circle(img,(int(px),int(py)),2,(255,255,255),-1)
    
        hough_img = img[:,:,0]

        lines = cv2.HoughLinesP(hough_img, 10, math.pi/180.0, 100, np.array([]), 45, 5)

        if lines is not None: 
            a,b,c = lines.shape


            for i in range(a):
                # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
                cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 5, cv2.LINE_AA)






if __name__=="__main__":

    rospy.init_node("le_scan")

    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)


    cv2.namedWindow("Saida")


    while not rospy.is_shutdown():
        print("Oeee")
        velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0.5))
        velocidade_saida.publish(velocidade)
        # Cria uma imagem 512 x 512
        branco = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        # Chama funćões de desenho
        desenha(branco)

        # Imprime a imagem de saida
        cv2.imshow("Saida", branco)
        cv2.waitKey(1)
        rospy.sleep(0.1)

```






