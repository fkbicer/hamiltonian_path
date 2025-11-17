# Hamiltonian Path Toolkit

This repository provides a structured implementation and benchmarking environment for the Hamiltonian s–t Path problem.  
The project was developed as part of the CMPE300 (Analysis of Algorithms) course at Boğaziçi University.

The codebase contains:

- A graph generator based on the assignment specification
- Three Hamiltonian path algorithms (naive, optimized, DP-based bonus)
- A measurement and benchmarking system
- A test suite using pytest
- A clean command-line interface (CLI)

---

## Project Structure
hamiltonian_path/
│
├── main.py
│
├── src/
│ ├── graph_generator.py
│ ├── solver.py
│ └── init.py
│
├── experiments/
│ ├── measurement.py
│ └── outputs/
│ ├── naive/
│ ├── optimized/
│ └── bonus/
│
├── tests/
│ ├── test_graph_generator.py
│ ├── test_small_graphs.py
│ ├── test_solver_selection.py
│ └── init.py
│
└── README.md
---

## Graph Model

The assignment specifies a graph with `3n` vertices, partitioned into three hidden components:

- Subgraph A: vertices `[0, n)`
- Subgraph B: vertices `[n, 2n)`
- Subgraph C: vertices `[2n, 3n)`

Each component is constructed by:

1. Creating a random spanning path  
2. Adding random edges with probability 1/2  
3. Randomly permuting all vertex labels  
4. Choosing distinct start and end nodes

Usage example:

```python
from src.graph_generator import GraphConstructor
graph, s, t = GraphConstructor().generate_tricky_graph(8)

## Algorithms

All algorithms are encapsulated inside the Solver class.

Naive Algorithm

Tries all permutations inside the induced subgraph.
Very slow due to factorial complexity.

Optimized Algorithm

Computes the connected component via BFS and restricts the search to that subset.

Bonus Algorithm (Bitmask DP)

A dynamic programming method similar to Held–Karp TSP DP.
Despite higher theoretical complexity, it performs well in practice.