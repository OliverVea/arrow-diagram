from models import *

import abc

class BaseGraphAnalyzer(abc.ABC):

    @abc.abstractstaticmethod
    def add_forward(graph: Graph) -> None:
        raise NotImplementedError()

    @abc.abstractstaticmethod
    def add_backward(graph: Graph) -> None:
        raise NotImplementedError()

class SequentialGraphAnalyzer(BaseGraphAnalyzer):
    def add_forward(graph: Graph) -> None:
        node_incoming_edges = {}

        for edge in graph.edges:
            node_incoming_edges.setdefault(edge.target, []).append(edge)
        
        graph.nodes[0].forward = 0

        for node in graph.nodes[1:]:
            incoming_edges = node_incoming_edges[node]
            costs = [edge.source.forward + edge.cost for edge in incoming_edges]
            node.forward = max(costs)

    def add_backward(graph: Graph) -> None:
        node_incoming_edges = {}

        for edge in graph.edges:
            node_incoming_edges.setdefault(edge.source, []).append(edge)
        
        graph.nodes[-1].backward = graph.nodes[-1].forward

        for node in reversed(graph.nodes[:-1]):
            incoming_edges = node_incoming_edges[node]
            costs = [edge.target.backward - edge.cost for edge in incoming_edges]
            node.backward = min(costs)