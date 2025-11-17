import pytest
from src.graph_generator import GraphConstructor


def test_generate_tricky_graph_basic():
    gc = GraphConstructor()
    graph, start, end = gc.generate_tricky_graph(4)  # N=12

    # graph size
    assert len(graph) == 12
    assert all(len(row) == 12 for row in graph)

    # entries are 0 or 1
    for row in graph:
        for val in row:
            assert val in (0, 1)

    # valid start/end
    assert 0 <= start < 12
    assert 0 <= end < 12
    assert start != end
