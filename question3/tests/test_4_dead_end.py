

import pytest
from mst.Mst import Graph, prims_mst

def test_simple():
    graph = Graph(4)
    graph.add_edge(0, 1, 4)
    graph.add_edge(2, 1, 4)
    result = prims_mst(graph)
    assert result == -1