# Semana de competição de drones

Nesta semana iremos trabalhar com o drone Bebop, da Parrot. Na aula de laboratório (terça ou quinta), iremos à quadra do 5o. andar do prédio 1 para participarmos de uma competição entre grupos. Para tanto os alunos deverão se organizar em grupos de 4 ou 5 integrantes (não precisam ser os mesmos do projeto).

Cada grupo irá usar o ROS instalado no próprio SSD para fazer o programa de controle do drone. Para tanto basta conectar ao drone correto e configurar o `IPberry` para o IP do notebook que roda o driver do drone. Esse notebook está preparado de acordo com o [guia](https://github.com/Insper/bebop_sphinx/blob/master/docs/bebop_tutorial.md#como-conectar-no-drone-se-voc%C3%AA-j%C3%A1-tem-o-bebop_autonomy-instalado) para se conectar ao Bebop real, que funciona apenas com o ROS Melodic e Ubunto 18.04.

No cenário da competição haverá quatro arucos impressos em papel A3 e presos no chão. Então cada grupo deverá escrever um Twist no tópico `/bebop2/camera_control` para fazer o drone olha para baixo (no máximo 80º). O objetivo da competição é criar um programa em Python que faça o drone sobrevoar os quatro arucos e completar a volta, fazendo o percurso no menor tempo possível. Para se orientar, o drone deve encontrar o próximo aruco, alinhar-se com ele e ir de encontro ao próximo aruco.

O desenvolvimento do programa deve ser realizado com o auxílio do simulador do Bebop. Siga os passos no [guia do simulador do Bebop] (https://github.com/Insper/404/blob/master/tutoriais/robotica/guia_drone_ros_noetic.md).

Após instalar o simulador, você pode simular um cenário com caixas através do comando abaixo:

```bash
roslaunch exemplos212 mav_fake_driver.launch 
```

Então faça o *take off* e execute o programa de exemplo, que está na pasta [ros/exemplos](./ros/exemplos).

```bash
rosrun exemplos221 visao_bebop.py 
```
Na aula de segunda-feira, recomendamos testar o controle de velocidade do drone simulado, fazer o programa que detecta a orientação do aruco e testar a conexão e os tópicos do drone real.

No dia da competição, cada grupo terá direito a 5 saídas com o drone, com o objetivo de ajustar as temporizações para a dinâmica do Bebop real e fazer a tomada de tempo

A documentação dos tópicos do drone real encontra-se em:
https://bebop-autonomy.readthedocs.io/en/latest/piloting.html


Não se esqueça de ter sempre um computador de backup com o seguinte comando pronto para parar o Bebop em caso de emergência:

```
rostopic pub --once /bebop/reset std_msgs/Empty
```

Boa sorte!


