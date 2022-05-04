
# Projeto 1

Deadline: 13/05/2022


## Missão:

O robô deverá fazer um tour de recohecimento do terreno e mapear as posições das bases, ou seja, das caixas contendo as imagens reconhecíveis através da MobileNet, usando as informações de odometria e do lidar e/ou da Intel Realsense. Então deverá ir até a reserva de creepers e pegar um creeper com ID e cor específicas, voltar à pista e levar até a base.

No percurso ao longo da pista o robô deve realizar um slalom passando entre as caixas azul e vermelha, continuando a seguir a pista depois disso


## Iniciando o projeto

Todos os integrantes do seu grupo deverão aceitar a tarefa no Github classroom que se encontra neste link:
https://classroom.github.com/a/ZO9q5lJt


Para criar a pasta do projeto, siga as instruções em:
https://github.com/Insper/robot22.1/blob/main/guides/projeto_rospython.md


Em especial atenção ao nome da pasta do reposório do projeto, como está especificado em:
https://github.com/Insper/robot22.1/blob/main/guides/projeto_rospython.md#usando-o-github-classroom


## Rubricas

**Conceito D - Mínimo para ter direito à Delta**

O robô percorre toda a pista, parando onde começou, usando
a odometria para saber de onde saiu e fazendo o slalom. É preciso gravar todo o circuito,  que deve ser percorrido em mendos de 30 min (tempo do simulador).


**Conceito C**

Robô é capaz de percorrer toda a pista, fazendo o *slalom*, parando onde começou.
É preciso realizar uma dentre duas tarefas:
 
1. Depois de dar volta, deve procurar e se chocar contra um creeper da cor certa e ID corretos, voltando depois à pista. A cor e o ID do creeper deve ser escolhida como um parâmetro do programa, ou seja, deve funcionar para qualquer cor e ID pedidos (desde a dupla seja válida); **ou** 
2. Percorrer a pista com o *slalom* usando o robô real. Caso seja necessário, a parede próxima às caixas vermelha e azul presente no simulador pode ser replicada com o auxílio de caixas.
 
É preciso gravar todo o circuito, que deve ser percorrido em menos de 30 min.

Para atingir este conceito, também é necessário demonstrar o trabalho em equipe, com commits equilibrados de todos os integrantes. Isso vale para todos os conceitos superiores também. 


**Conceito C+**

Robô é capaz de percorer toda a pista, fazendo o slalom, parando onde começou. Depois, deve procurar e "encostar" em um creeper da cor certa e ID corretos, voltando depois à pista. A cor e o ID do creeper deve ser escolhida como um parâmetro do programa, ou seja, deve funcionar para qualquer cor e ID pedidos (desde a dupla seja válida). É preciso gravar todo o circuito, que deve ser percorrido em mendos de 30 min.

Encostar no creeper significa, especificamente: chegar bem perto do creeper com a garra abaixada, e então parar o robô e levantar a garra.

É preciso gravar todo o circuito, que deve ser percorrido em mendos de 30 min. Também é preciso comprovar o trabalho em equipe. 


**Conceito B** 

O robô deve percorrer toda a pista, parando onde começou, e no meio do caminho pega o creeper da cor e ID corretos com a garra e volta para a pista. 

A cor e o ID devem ser parâmetros do programa, ou seja, ele deve funcionar para qualquer valor de cor e ID. 

O código tem que estar bem modularizado em comportamentos, e cada função/método deve estar documentada explicando de forma resumida o que faz, como no exemplo abaixo:

```python

def soma(a,b):
	“””
	Retorna a soma de a e b
	”””
  	return a + b
```

É preciso gravar todo o circuito, que deve ser percorrido em mendos de 30 min.

**Conceito B+** 

Além dos itens do conceito B, o robô deve deixar o creeper na na base certa e completar mais uma volta na pista.
A base também deve ser fornecida como parâmetro do projeto. 


**Conceito A**

Itens do conceito B+ mais o uso de classes e objetos Python    

Só pode ter sleep dentro do `while` principal. 

Fazer um dentre os quatro *especiais*:
* Gravar e filmar no robô real funcionado
* Fazer um controle proporcional para manter o robô na pista, alinhar pelo creeper e pela base, e fazer funcionar rápido baseado no ângulo de visão da pista.
* Mapear os Arucos da pista e dos creepers usando o modo 3D e odometria.
* Estruturar o programa com pelo menos um node ROS prestando serviço para o outro.

**Conceito A+**

Itens do conceito A e fazer 3 especiais em vez de apenas um.

**Conceito A+ para grupos de 4**

Itens do conceito A e fazer todos os 4 especiais

### Grupos de 4 pessoas 

Os grupos de 4 pessoas terão sempre um conceito deslocado em relacão aos de 3 pessoas.

Para obter A+ num grupo de 4, é necessário  fazer os 4 especiais.

Assim, o necessário para conceito B em grupos de 3 representa o conceito C+ em grupos de 4.


### Uso do robô real

Caso o projeto seja apresentado no robô real, a nota subirá um conceito relativamente ao que foi entregue. Assim, caso for cumprida a rubrica do conceito C para o seu grupo, tiver sido utilizado o robô real, a nota do projeto será um **C+**. 


<img src="./pista virtual.png">


# Objetivos 




### Exemplos de objetivos da missão (devem ser filmados): 

Cores válidas do creeper: `blue`, `green`, `pink`.

Estações válidas: `horse`, `bird` e `bicycle`

Os objetivos abaixo são exemplos de objetivos possíveis,  eque devem ser filmados para fins de demonstração.  O seu robô deve ser capaz de realizar *qualquer* objetivo. 


```python
goal1 = ("blue", 22, "bird")

goal2 = ("green", 13, "bicycle")

goal3 = ("pink", 11, "horse")
```


Por exemplo, o objetivo `("blue", 22, "bird")` significa *Encontre o creeper azul de ID 22 e o traga até a caixa com figura de pássaro*. 


# Instruções

Comandos para atualizar os repositório
```bash
    cd ~catkin_ws/src/mybot_description
    git pull
    cd ~catkin_ws/src/my_simulation
    git pull
    cd ~catkin_ws/src/robot22.1
    git pull
```

Para executar:

	roslaunch my_simulation projeto_2022.launch

Para habilitar o controle da garra executar:

	roslaunch mybot_description mybot_control2.launch 	


Como atividade inicial, sugiro que tente fazer o robô *seguir a pista* . Você pode se basear em sua Atividade 3, ou ainda desenvolver uma abordagem baseada em centro de massa da linha amarela, como [encontrada neste link](https://github.com/osrf/rosbook/blob/master/followbot/follower_color_filter.py)


# Exemplo do ARUCO 

Exemplo de como interpretar os markers ARUCO 
[./aruco/aruco.ipynb] (./aruco/aruco.ipynb)

Exemplo de como programar usando os markers ARUCO em 3D 
[https://github.com/Insper/robot22.1/blob/main/projeto/aruco/aruco.py](https://github.com/Insper/robot22.1/blob/main/projeto/aruco/aruco.py)

# Instruções sobre os tópicos da garra 

[Fonte: https://github.com/arnaldojr/mybot_description/](https://github.com/arnaldojr/mybot_description/)

Launch para subir os controles da garra e RViz

        roslaunch mybot_description mybot_control2.launch 

Para publicar um topico da garra:

Joint1 = braço da garra. Valores máximos:

    Garra recolhida: -1
    Garra para frente: 0
    Garra levantada: 1.5
    
    No terminal:
        rostopic pub -1 /joint1_position_controller/command std_msgs/Float64 "data: 0"
    
Joint2 = Pinça da garra.

    Pinça fechada: 0
    Pinça aberta: -1
    
    No terminal:
        rostopic pub -1 /joint2_position_controller/command std_msgs/Float64 "data: 0"
    
Visualizar arvore:

    rosrun rqt_gui rqt_gui 
    
Exemplo de codigo py:

[https://github.com/Insper/robot22.1/blob/main/ros/exemplos_221/scripts/garra_simples.py](https://github.com/Insper/robot22.1/blob/main/ros/exemplos_221/scripts/garra_simples.py)


