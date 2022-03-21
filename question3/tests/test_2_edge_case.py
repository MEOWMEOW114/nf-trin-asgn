

import pytest
from mst.Mst import Graph, prims_mst

def test_simple():
    g = Graph(4)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 2, 6)
    g.add_edge(0, 3, 5)
    g.add_edge(1, 3, 15)
    g.add_edge(2, 3, 4)
    result = prims_mst(g)
    assert result == 19