""" 
Executa a busca em um mapa com custo fixo

"""
from busca_base import GridWithAdjustedWeights
from busca_largura import BuscaLargura
from busca_dijkstra import BuscaDijkstra

MAP_NAME = "map.png"

def main():

    mapa = GridWithAdjustedWeights(MAP_NAME)

    busca = BuscaLargura()

    busca.do_search(mapa, start = (120,120), goal = (90, 90)) 


if __name__ == "__main__":
    main()

