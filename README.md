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

```
hamiltonian_path/
│
├── main.py
│
├── src/
│   ├── graph_generator.py
│   ├── solver.py
│   └── __init__.py
│
├── experiments/
│   ├── measurement.py
│   └── outputs/
│       ├── naive/
│       ├── optimized/
│       └── bonus/
│
├── tests/
│   ├── test_graph_generator.py
│   ├── test_small_graphs.py
│   ├── test_solver_selection.py
│   └── __init__.py
│
└── README.md
```

---

## 1- Graph Model

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
```

---

## 2- Algorithms

All algorithms are encapsulated inside the `Solver` class.

### 2.1- Naive Algorithm

Tries all permutations inside the induced subgraph.  
Very slow due to factorial complexity.

### 2.2- Optimized Algorithm

Computes the connected component via BFS and restricts the search to that subset.

### 2.3- Bonus Algorithm (Bitmask DP)

A dynamic programming method similar to Held–Karp TSP DP.  
Despite higher theoretical complexity, it performs well in practice.


## 3- Measurement and Benchmarking

The measurement runner performs:

- Graph generation
- Multiple trials per n value
- CSV output
- Plot generation (PNG)

Outputs are saved under:

```
experiments/outputs/<algorithm>/
```

### Running an experiment:

```
python main.py measure --algorithm naive --n-list 4 5 6 7 --trials 3
```

This produces:

- A CSV file with timestamped metrics  
- A plot showing execution time vs. n  

---

## 4- Command Line Usage

### Solve a single instance:

```
python main.py solve --algorithm naive --n 8
```

Example output:

```
=== HAMILTONIAN PATH SOLVER ===
Algorithm  : naive
Start node : 12
End node   : 2
Result     : FOUND
================================
```

### Run measurements:

```
python main.py measure --algorithm optimized --n-list 6 7 8 --trials 5
```

---

## Running Tests

Run all tests using pytest:

```
pytest -q
```

The test suite includes:

- Graph generation tests
- Small graph correctness tests
- Solver algorithm-selection tests

---

## Example Output Tree

```
experiments/outputs/naive/
│
├── csv/
│   ├── naive_results_20251117_153045.csv
│
└── plots/
    ├── naive_plot_20251117_153045.png
```