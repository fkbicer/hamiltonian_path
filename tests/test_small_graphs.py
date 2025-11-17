import pytest
from src.solver import Solver

def test_small_graph_naive_not_applicable():
    graph = [
        [0,1,0],
        [1,0,1],
        [0,1,0]
    ]

    solver = Solver(graph, 0, 2)

    # naive algorithm is NOT expected to run on N=3 graphs
    with pytest.raises(ValueError):
        solver.execute("naive")


def test_small_graph_exists_optimized():
    graph = [
        [0,1,0],
        [1,0,1],
        [0,1,0]
    ]
    solver = Solver(graph, 0, 2)
    assert solver.execute("optimized") is True


def test_small_graph_not_exists_optimized():
    graph = [
        [0,1,0],
        [1,0,0],
        [0,0,0]
    ]
    solver = Solver(graph, 0, 2)
    assert solver.execute("optimized") is False
