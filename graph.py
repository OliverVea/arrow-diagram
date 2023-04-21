from models import *

import string
import networkx

from random import normalvariate, randint

def _get_cost():
    return int(abs(normalvariate(mu = 1, sigma = 5)))

def get_name(i: int, task_count: int):
    if task_count <= len(string.ascii_lowercase):
        return string.ascii_uppercase[i]
    return str(i + 1)

def generate_graph(task_count: int, edge_count: int) -> Graph:
    nodes = [Node(get_name(i, task_count), None) for i in range(task_count)]
    edges = []

    def add_edge(edge: Edge):
        edges.append(edge)
        graph.add_edge(edge.source.name, edge.target.name)

    graph = networkx.Graph()

    for i in range(task_count - 1):
        add_edge(Edge(nodes[i], nodes[i+1], _get_cost()))

    counter = edge_count

    while counter > 0:
        i_u = randint(0, len(nodes) - 1)
        i_v = randint(0, len(nodes) - 1)

        u = nodes[i_u]
        v = nodes[i_v]

        if i_u >= i_v or graph.has_edge(u.name, v.name):
            continue

        counter -= 1

        add_edge(Edge(u, v, _get_cost()))
    
    #layout = networkx.layout.spring_layout(graph, pos={nodes[i].name: (i,i/10) for i in range(len(nodes))}, scale=10)  
    layout = networkx.layout.kamada_kawai_layout(graph, scale=10)

    for node in nodes:
        position = layout[node.name]
        node.position = tuple(position)
    
    return Graph(nodes, edges)