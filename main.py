import argparse
from src.graph_generator import GraphConstructor
from src.solver import Solver
from experiments.measurement import Measurement


def cli_solve(args):
    """
    Handle: python main.py solve --algorithm naive --n 8
    """
    gc = GraphConstructor()
    graph, start, end = gc.generate_tricky_graph(args.n)

    solver = Solver(graph, start, end)
    result = solver.execute(args.algorithm)

    print("\n=== HAMILTONIAN PATH SOLVER ===")
    print(f"Algorithm  : {args.algorithm}")
    print(f"Start node : {start}")
    print(f"End node   : {end}")
    print(f"Result     : {'FOUND' if result else 'NOT FOUND'}")
    print("================================\n")


def cli_measure(args):
    """
    Handle: python main.py measure --algorithm naive --n-list 4 5 6 --trials 3
    """
    runner = Measurement(args.algorithm)

    # n-list verilmişse onu kullan
    n_values = args.n_list

    # n-list verilmemişse default değer ata
    if not n_values:
        if args.algorithm == "naive":
            n_values = [4, 5, 6, 7]
        elif args.algorithm == "optimized":
            n_values = [6, 7, 8, 9]
        else:  # bonus
            n_values = [10, 11, 12, 13]

    runner.run_experiment(n_values, trials=args.trials)


def main():
    parser = argparse.ArgumentParser(
        description="Hamiltonian Path Toolkit (Solver + Measurement)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ----------------------------------------------------------------------
    # solve subcommand
    # ----------------------------------------------------------------------
    solve_parser = subparsers.add_parser(
        "solve",
        help="Generate a graph & check Hamiltonian path."
    )
    solve_parser.add_argument(
        "--algorithm",
        type=str,
        choices=["naive", "optimized", "bonus"],
        required=True
    )
    solve_parser.add_argument(
        "--n",
        type=int,
        required=True,
        help="Subgraph size (total graph size = 3*n)"
    )
    solve_parser.set_defaults(func=cli_solve)

    # ----------------------------------------------------------------------
    # measure subcommand
    # ----------------------------------------------------------------------
    measure_parser = subparsers.add_parser(
        "measure",
        help="Run performance measurements for algorithms."
    )
    measure_parser.add_argument(
        "--algorithm",
        type=str,
        choices=["naive", "optimized", "bonus"],
        required=True
    )
    measure_parser.add_argument(
        "--n-list",
        nargs="*",
        type=int,
        help="List of n values, e.g. --n-list 4 5 6"
    )
    measure_parser.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Number of repeated runs per n value"
    )
    measure_parser.set_defaults(func=cli_measure)

    # Run command
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
