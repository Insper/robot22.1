# Projeto Busca

Veja a [aula sobre busca](./Busca.pdf).

O objetivo deste projeto é implementar a busca A* no Turtlebot para que encontre o melhor caminho até o local designado, a ser sorteado em sala de aula. O replanejamento e execução da trajetória ficam por conta do ROS. Para evitar que a odometria do robô se perca, vamos fazer a localização por filtro de partículas, usando o mapa obtido por meior de SLAM (Simultaneous Localization and Mapping).  

## Entregas: 
- Código do projeto de busca no github classroom (aguardar o starter code)
    - O grupo do projeto de busca deverá ser o mesmo do projeto anterior
- Video do robô simulado mapeando o cenário do projeto
- Video do robô real ou simulado percorrendo o trajeto planejado (link)
- Video da tela do RViz (link)

## Avaliação

Este projeto possui rubrica única, com avaliação binária (passou ou não passou).

Os grupos que filmarem a execução da trajetória com o robô real terão um acréscimo de meio conceito na nota de projeto. 

Este projeto é de entrega obrigatória.

## O que deverá ser feito

1. Implemente a busca A* no arquivo `busca_astar.py`. Para testar, altere o programa `roda_busca.py`. Enquanto não receber o starter code do projeto, trabalhe em cima dos arquivos fornecidos nesta pasta. Faça testes em seu código com diferentes posições de `start`e `goal`e discuta com o grupo:

    - O que pode ser feito para o código executar mais rápido?
    - Quando a heurística ajuda mais?
    - Só a heurística como função de priorização pode atrapalha?


2. Mapeie o cenário do projeto usando o algortimo `gmapping`. Veja o tutorial em https://github.com/Insper/404/blob/master/tutoriais/robotica/navigation_gazebo_simulador.md. Não esqueça de filmar o robô simulado e o RViz. Carregue o cenário com o comando:

        roslaunch my_simulation projeto_2020.launch

3. Faça a navegação do robô real ou simulado com o comando:

        roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=<arquivo_mapa>
    
    Importante:
    
    - Você deverá iniciar o simulador ou *bringup* com o robô real antes de executar a navegação
    - O arquivo do mapa será diferente para o robô real ou o simulado. O mapa do ambiente real será fornecido.
    - Não esqueça de filmar a execução da trajetória pelo robô e na tela do RViz.




