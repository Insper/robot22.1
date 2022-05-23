""" 
Implementação da busca em largura a partir das interfaces em busca_base.py
"""

from busca_base import FrontierInterface, AbstractSearchBase, Location

import collections

class Queue(FrontierInterface):
    """ Classe que implementa uma fila (FIFO) para a busca em largura"""
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: Location, total_cost: float):
        self.elements.append(x)
    
    def get(self) -> Location:
        return self.elements.popleft()



class BuscaLargura(AbstractSearchBase):
    """ Classe que implementa os métodos faltantes na busca básica """

    def create_empty_frontier(self) -> FrontierInterface:
        """Cria uma nova lista de nós abertos (fronteira) com base no tipo de busca"""
        return Queue()

    def calculate_priority(self, current: Location, cost: float, goal: Location) -> float:
        """Calcula a função avaliação para a prioridade do nó"""
        return 0

