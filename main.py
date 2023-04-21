# Imports
from models import *
from graph import generate_graph
from analysis import SequentialGraphAnalyzer
from drawing import draw_graph

from time import perf_counter

import pathlib

# Configuration
NODE_COUNT = 8
EDGE_COUNT = 4

TO_LOAD = 'latest.json'
TO_LOAD = None

DRAW = ['before', 'forward', 'backward']

ANALYZER = SequentialGraphAnalyzer

PATH = pathlib.Path(__file__).parent / 'data'

# Logic
if TO_LOAD: graph = Graph.load(PATH / TO_LOAD)
else: graph = generate_graph(NODE_COUNT, EDGE_COUNT)

graph.save(PATH / 'latest.json')

if 'before' in DRAW: draw_graph(graph)

forward_start = perf_counter()
ANALYZER.add_forward(graph)
forward_time = perf_counter() - forward_start
print(f'forward analysis took {forward_time:.2f} seconds')

if 'forward' in DRAW: draw_graph(graph)

backward_start = perf_counter()
ANALYZER.add_backward(graph)
backward_time = perf_counter() - backward_start
print(f'backward analysis took {backward_time:.2f} seconds')

if 'backward' in DRAW: draw_graph(graph)
