from models import *

from schemdraw import Drawing
from schemdraw.flow import Circle
from schemdraw.flow import Arrow as Line

from math import atan2, pi, cos, sin

def draw_graph(graph: Graph, circle_radius: float = 0.85):

    with Drawing() as d:
        node_lookup: dict[Node, Circle] = {}
        for i, node in enumerate(graph.nodes):
            node_lookup[node] = Circle(r=circle_radius).label(node.label()).at(node.position)

            if i == 0:
                node_lookup[node].color('green')

            d.add(node_lookup[node])

        edge_lookup: dict[Edge, Line] = {}
        for edge in graph.edges:
            source_node = node_lookup[edge.source]
            target_node = node_lookup[edge.target]

            x = edge.target.position[0] - edge.source.position[0]
            y = edge.target.position[1] - edge.source.position[1]

            angle = atan2(y, x)

            at = (cos(angle) * circle_radius + source_node.center[0], sin(angle) * circle_radius + source_node.center[1])
            to = (cos(angle + pi) * circle_radius + target_node.center[0], sin(angle + pi) * circle_radius + target_node.center[1])

            edge_lookup[edge] = Line().at(at).to(to)

            if edge.cost > 0:
                edge_lookup[edge].label(str(edge.cost))
            else:
                edge_lookup[edge].style(ls='--')

            d.add(edge_lookup[edge])
        
        d.draw()