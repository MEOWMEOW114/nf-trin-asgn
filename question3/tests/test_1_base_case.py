

import pytest
from mst.Mst import Graph, prims_mst

def test_simple():
    graph = Graph(4)
    graph.add_edge(0, 1, 4)
    graph.add_edge(2, 1, 1)
    graph.add_edge(2, 3, 2)
    graph.add_edge(3, 0, 5)
    result = prims_mst(graph)
    assert result == 7