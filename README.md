Hamiltonian Path Toolkit

This repository provides a modular, well-structured implementation and benchmarking environment for the Hamiltonian s–t Path problem. The project was developed as part of the CMPE300 (Analysis of Algorithms) course at Boğaziçi University.

The goal of the project is to analyze different algorithmic approaches to the Hamiltonian path problem under a specific graph-generation model provided by the course instructors. This repository includes clean implementations of multiple algorithms, a measurement suite, a full command-line interface (CLI), and an automated testing framework.

Project Structure
hamiltonian_path/
│
├── main.py                          # Command-line interface (solve + measure)
│
├── src/
│   ├── graph_generator.py           # GraphConstructor class
│   ├── solver.py                    # Solver class (naive, optimized, bonus)
│   └── __init__.py
│
├── experiments/
│   ├── measurement.py               # Measurement class (benchmarking)
│   └── outputs/                     # Auto-generated plots and CSV files
│       ├── naive/
│       ├── optimized/
│       └── bonus/
│
├── tests/                           # Unit tests (pytest)
│   ├── test_graph_generator.py
│   ├── test_small_graphs.py
│   ├── test_solver_selection.py
│   └── __init__.py
│
└── README.md

Graph Model

The assignment specifies a particular random graph construction method. For a chosen parameter n, the graph has 3n vertices, partitioned into three independent subgraphs A, B, and C, each of size n.

Each subgraph is constructed as follows:
A random spanning path is generated to ensure connectivity.
Additional edges are added independently with probability 1/2.
The entire graph is then uniformly relabeled with a random permutation so that the three-block structure is not visible.
Distinct start and end vertices are selected uniformly at random.
The construction logic is encapsulated in:

from src.graph_generator import GraphConstructor
graph, s, t = GraphConstructor().generate_tricky_graph(n)

Algorithms
All algorithms are implemented inside the Solver class. Users may select the algorithm via the CLI or programmatically.
1. Naive Algorithm
The naive method iterates over all permutations of the nodes inside the relevant induced subgraph and checks whether any permutation forms a Hamiltonian s–t path.
This method is extremely slow even for modest n values because of factorial growth.
2. Optimized Algorithm
The optimized method first identifies the connected component containing the start vertex via BFS. If the end vertex is not in the same component, no Hamiltonian path can exist.
If both vertices are in the same component, the algorithm extracts the induced subgraph and performs a restricted permutation search.
3. Bonus Algorithm (DP Bitmask Method)
This method uses a dynamic programming approach similar to the classical Held–Karp algorithm for TSP. It maintains a DP table indexed by subsets of vertices and endpoints, and tries to extend partial paths.
Although its asymptotic complexity is higher, it performs very efficiently in practice due to predictable memory access patterns, low constant factors, and tight control flow.

Measurement Framework

The benchmarking framework is located in:
experiments/measurement.py

It performs the following tasks:
Generates tricky graphs for selected n values
Executes the chosen algorithm multiple times (trials)
Records results and execution times into timestamped CSV files
Produces plots of average execution time vs. n

Stores outputs in structured folders:
experiments/outputs/<algorithm>/csv/
experiments/outputs/<algorithm>/plots/

Example CSV filename:
naive_results_20251117_153045.csv

Example plot filename:
naive_plot_20251117_153045.png

Command-Line Usage
The entire project is managed via a user-friendly CLI defined in main.py.
1. Solve a Single Instance
Generate a random graph of size 3n and test a selected algorithm:

python main.py solve --algorithm naive --n 8

Output example:

=== HAMILTONIAN PATH SOLVER ===
Algorithm  : naive
Start node : 12
End node   : 2
Result     : FOUND
================================

Available algorithms:

naive
optimized
bonus

2. Run Performance Measurements
Test an algorithm for multiple n values:

python main.py measure --algorithm naive --n-list 4 5 6 7 --trials 3

This will run each n value 3 times, record results, and generate a plot and CSV file.
If the user does not specify n values, defaults are used:
naive: 4, 5, 6, 7
optimized: 6, 7, 8, 9
bonus: 10, 11, 12, 13

Running Tests
The project includes an automated test suite using pytest.
Run all tests:

pytest -q

Tests include:
Graph generation correctness
Algorithm selection via the solver class
Correct detection of simple Hamiltonian paths

Example Output Snapshot
After running measurements, the output directory may look like:

experiments/outputs/naive/
│
├── csv/
│   ├── naive_results_20251117_153045.csv
│   └── naive_results_20251117_153530.csv
│
└── plots/
    ├── naive_plot_20251117_153045.png
    └── naive_plot_20251117_153530.png
