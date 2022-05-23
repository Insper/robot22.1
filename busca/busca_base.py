"""
Implementação do planejamento de trajetória usando busca.
Neste arquivo são definidas as interfaces e as classes de base.

Implementação baseada no código origonal:
https://www.redblobgames.com/pathfinding/a-star/implementation.py

Explicação em (vale a leitura!):
https://www.redblobgames.com/pathfinding/a-star/implementation.html


Copyright 2014 Red Blob Games <redblobgames@gmail.com>

License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>

Author : Antonio Selvatici <antoniohps1@insper.edu.br>

"""

from __future__ import annotations

import cv2
import numpy as np

# some of these types are deprecated: https://www.python.org/dev/peps/pep-0585/
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional

T = TypeVar('T')

Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass

class SimpleGraph:
    def __init__(self):
        self.edges: Dict[Location, List[Location]] = {}
    
    def neighbors(self, id: Location) -> List[Location]:
        return self.edges[id]

import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, x: T):
        self.elements.append(x)
    
    def get(self) -> T:
        return self.elements.popleft()

# utility functions for dealing with square grids
def from_id_width(id, width):
    return (id % width, id // width)

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

GridLocation = Tuple[int, int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []
        self.image = np.ones((height, width, 3), dtype=np.uint8)*255
    
    def __init__(self, fname: str):
        img = cv2.imread(fname, cv2.IMREAD_COLOR)
        self.height, self.width, _ = img.shape
        self.image = img
        self.walls: List[GridLocation] = []

        iLin, iCol, _ = np.where(img < 20)

        for lin, col in zip(iLin, iCol):
            self.walls.append((col, lin))

    def save(self, fname):
        cv2.imwrite(fname, self.image)

    def set_start(self, id: GridLocation):
        cv2.circle(self.image, id, 3, (0,255,0), -1)

    def set_goal(self, id: GridLocation):
        cv2.circle(self.image, id, 3, (0,0,255), -1)

    def set_closed(self, id: GridLocation):
        self.image[id[1], id[0]] = (100,100,100)

    def set_path(self, id: GridLocation):
        self.image[id[1], id[0]] = (255,50,50)

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}

    def __init__(self, pgm: str):
        super().__init__(pgm)
        self.weights: Dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)


# thanks to @m1sp <Jaiden Mispy> for this simpler version of
# reconstruct_path that doesn't have duplicate entries

def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:

    current: Location = goal
    path: List[Location] = []
    while current != start: # note: this will fail if no path found
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


class GridWithAdjustedWeights(GridWithWeights):
    def cost(self, from_node, to_node):
        prev_cost = super().cost(from_node, to_node)
        nudge = 0
        (x1, y1) = from_node
        (x2, y2) = to_node
        if (x1 + y1) % 2 == 0 and x2 != x1: nudge = 1
        if (x1 + y1) % 2 == 1 and y2 != y1: nudge = 1
        return prev_cost + 0.001 * nudge


class FrontierInterface:
    def put(self, node: Location, total_cost: float):
        raise NotImplementedError
 
    def empty(self) -> bool:
        raise NotImplementedError

    def get(self) -> Location:
        raise NotImplementedError


class AbstractSearchBase:
    """
    Classe que define os métodos básicos de busca. 
    As classes detivadas deverão implementar os métodos:
    - create_empty_list(self)

    """

    def create_empty_frontier(self) -> FrontierInterface:
        """Cria uma nova lista de nós abertos (fronteira) com base no tipo de busca"""
        raise NotImplementedError

    def calculate_priority(self, current: Location, cost: float, goal: Location) -> float:
        """Calcula a função avaliação para a prioridade do nó"""
        raise NotImplementedError

    def do_search(self, graph: GridWithWeights, start: GridLocation, goal: GridLocation):
        
        frontier = self.create_empty_frontier()
        frontier.put(start, 0)
        came_from: Dict[GridLocation, Optional[GridLocation]] = {}
        cost_so_far: Dict[GridLocation, float] = {}
        came_from[start] = None
        cost_so_far[start] = 0
        

        while not frontier.empty():
            current: GridLocation = frontier.get()
            graph.set_closed(current)
            
            if current == goal:
                break
            
            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = self.calculate_priority(next, new_cost, goal)
                    frontier.put(next, priority)
                    came_from[next] = current

        path = reconstruct_path(came_from, start, goal) 
        for loc in path:
            graph.set_path(loc)

        graph.set_start(start)
        graph.set_goal(goal)
        graph.save("caminho_salvo.png")

        return path
