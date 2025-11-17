from src.solver import Solver


def test_solver_selects_correct_algorithm(monkeypatch):
    # dummy trivial graph
    graph = [
        [0,1,0],
        [1,0,1],
        [0,1,0]
    ]
    s = 0
    t = 2

    solver = Solver(graph, s, t)

    # Patch internal algorithms so we know which is called
    called = {"naive": False, "optimized": False, "bonus": False}

    monkeypatch.setattr(solver, "_Solver__naive", lambda: called.__setitem__("naive", True))
    monkeypatch.setattr(solver, "_Solver__optimized", lambda: called.__setitem__("optimized", True))
    monkeypatch.setattr(solver, "_Solver__bonus", lambda: called.__setitem__("bonus", True))

    solver.execute("naive")
    assert called["naive"] is True
    assert called["optimized"] is False
    assert called["bonus"] is False

    # reset
    called = {"naive": False, "optimized": False, "bonus": False}

    solver.execute("optimized")
    assert called["optimized"] is True
    assert called["naive"] is False
    assert called["bonus"] is False

    # reset
    called = {"naive": False, "optimized": False, "bonus": False}

    solver.execute("bonus")
    assert called["bonus"] is True
