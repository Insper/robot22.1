# Semana 04 - Introdução ao ROS

**Aviso**: você precisará do SSD com Linux de agora em diante

## Conteúdo

Ouça a explicação e demonstrações do professor sobre o ROS. Além disso, consulte os guias de referência para saber os passos necessários à execução do ROS. Aqui temos apenas referências rápidas aos comandos a serem executados depois que o setup estiver completo.  

1. **Testando o ROS:** simulador Gazebo + Teleop
    
        export TURTLEBOT3_MODEL=waffle_pi
        roslaunch turtlebot3_gazebo turtlebot3_house.launch

        roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch

1. **Vendo os dados de sensores do robô**
        
        rqt_image_view

        roslaunch turtlebot3_gazebo turtlebot3_gazebo_rviz.launch

1. **O que são tópicos** e como ler e escrever neles

        rostopic list <topic>
        rostopic echo <topic>
        rostopic pub <topic> ...

1. **O que são `nodes`** e sua relação com os *tópicos*

        rostopic info <topic>
        rqt_graph

1. **Packages**:

        roscd <package>
        roslaunch <package> <launch file>
        rosrun <package> <program>
        catkin_make

1. **Ler sensores**
        
        rosrun exemplos_221 le_scan.py
        rosrun exemplos_221 print_odom.py
        rosrun exemplos_221 processa_imagem.py
        
1. **Mover o robô**

        rosrun exemplos_221 roda.py

## Para praticar

Modifique o programa de exemplo `processa_imagem.py` e `cor_module.py` para que gire o robô até encontrar o maior objeto verde (sem sair do lugar), centralize a visada do robô no centro do contorno e pare. Para tanto use o seguinte cenário:

        roslaunch turtlebot3_gazebo turtlebot3_world.launch


## Guias de referência do ROS

[1 - Simulador Gazebo](./guides/simulador_ros.md)

[2 - ROS topics - como explorar](./guides/ros_topics.md)

[3 - Parar o robô via terminal](./guides/parar_robo.md)

[4 - Como criar um projeto Ros Python](./guides/projeto_rospython.md)

**Dica**: os exemplos mencionados no guia estão no pacote `exemplos_221`. Para utilizá-los, certificar-se de que os scripts Python são executáveis:

    chmod a+x `rospack find exemplos212`/scripts/*.py

https://github.com/Insper/robot21.2/blob/main/guides/ros_topics.md

ROS Robot Programming - capítulos 5 e 6: https://community.robotsource.org/t/download-the-ros-robot-programming-book-for-free/51





