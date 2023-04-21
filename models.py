from dataclasses import dataclass, asdict
from pathlib import Path

import json

@dataclass
class Node:
    name: str
    position: tuple[float, float]

    forward: int | None = None
    backward: int | None = None

    def __hash__(self) -> int:
        return self.__str__().__hash__()
    
    def label(self) -> str:
        forward = str(self.forward) if self.forward != None else "  "
        backward = str(self.backward) if self.backward != None else "  "

        components = [self.name, f'[{forward}/{backward}]']
        return '\n'.join(components)

@dataclass
class Edge:
    source: Node
    target: Node
    cost: int

    def __hash__(self) -> int:
        return self.__str__().__hash__()

@dataclass
class Graph:
    nodes: list[Node]
    edges: list[Edge]

    @staticmethod
    def load(path: Path):
        with open(path, 'r') as f:
            dict = json.load(f)
        
        node_lookup = {data['name']: Node(**data) for data in dict['nodes']}
        edges = [Edge(node_lookup[data['source']], node_lookup[data['target']], data['cost']) for data in dict['edges']]
        nodes = list(node_lookup.values())

        return Graph(nodes, edges)
    
    def save(self, path: Path) -> None:
        dict = {
            'nodes': [asdict(node) for node in self.nodes],
            'edges': [
                {
                    'source': edge.source.name,
                    'target': edge.target.name,
                    'cost': edge.cost
                } for edge in self.edges ]
        }

        with open(path, 'w') as f:
            json.dump(dict, f, indent=4)
