
import heapq

from busca_base import List, Tuple, T, GridLocation, FrontierInterface, AbstractSearchBase

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]



class BuscaDijkstra(AbstractSearchBase):
    """ Classe que implementa os métodos faltantes na busca básica """

    def create_empty_frontier(self) -> FrontierInterface:
        """Cria uma nova lista de nós abertos (fronteira) com base no tipo de busca"""
        return PriorityQueue()

    def calculate_priority(self, current: GridLocation, cost: float, goal: GridLocation) -> float:
        """Calcula a função avaliação para a prioridade do nó"""
        return cost + abs(goal[0]-current[0]) + abs(goal[1]-current[1]) 