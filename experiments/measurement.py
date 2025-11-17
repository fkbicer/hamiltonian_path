import time
import os
import csv
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

from src.graph_generator import GraphConstructor
from src.solver import Solver


class Measurement:
    """
    Flexible experiment runner for all Hamiltonian Path algorithms.
    """

    def __init__(self, algorithm):
        if algorithm not in ("naive", "optimized", "bonus"):
            raise ValueError("Algorithm must be naive / optimized / bonus.")
        self.algorithm = algorithm

        # Output directories
        self.base_dir = os.path.join("experiments", "outputs", algorithm)
        self.plots_dir = os.path.join(self.base_dir, "plots")
        self.csv_dir = os.path.join(self.base_dir, "csv")

        os.makedirs(self.plots_dir, exist_ok=True)
        os.makedirs(self.csv_dir, exist_ok=True)

    def run_experiment(self, n_values, trials=3):
        gc = GraphConstructor()
        avg_times = []

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        csv_path = os.path.join(
            self.csv_dir,
            f"{self.algorithm}_results_{timestamp}.csv"
        )

        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["algorithm", "n", "trial", "result", "time_sec"])

            for n in n_values:
                print(f"\n[{self.algorithm.upper()}] Running for n={n} ...")
                run_times = []

                for trial in range(trials):
                    graph, s, t = gc.generate_tricky_graph(n)
                    solver = Solver(graph, s, t)

                    t0 = time.perf_counter()
                    result = solver.execute(self.algorithm)
                    t1 = time.perf_counter()

                    elapsed = (t1 - t0)
                    run_times.append(elapsed)

                    writer.writerow([self.algorithm, n, trial + 1, result, elapsed])
                    print(f"  Trial {trial+1}: {elapsed:.5f} sec")

                avg_time = sum(run_times) / len(run_times)
                avg_times.append(avg_time)
                print(f"  Average time: {avg_time:.6f} sec")

        plot_path = self._plot_results(n_values, avg_times, timestamp)

        print(f"\nSaved CSV → {csv_path}")
        print(f"Saved Plot → {plot_path}\n")

        return csv_path, plot_path

    def _plot_results(self, n_values, avg_times, timestamp):
        plt.figure(figsize=(9, 6))
        plt.plot(n_values, avg_times, marker="o", linestyle="-", color="blue")

        plt.xticks(n_values)
        plt.xlabel("n (subgraph size)")
        plt.ylabel("Average Execution Time (sec)")
        plt.title(f"{self.algorithm.capitalize()} Algorithm Execution Time")
        plt.grid(True)

        for x, y in zip(n_values, avg_times):
            plt.text(x, y, f"{y:.4f}", ha="center", va="bottom", fontsize=9)

        plot_path = os.path.join(
            self.plots_dir,
            f"{self.algorithm}_plot_{timestamp}.png"
        )

        plt.savefig(plot_path, dpi=300)
        plt.close()
        return plot_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", type=str, required=True,
                        choices=["naive", "optimized", "bonus"])
    parser.add_argument("--n-list", nargs="*", type=int,
                        help="Optional custom n values (ex: --n-list 4 5 6 7 8)")
    parser.add_argument("--trials", type=int, default=1)

    args = parser.parse_args()

    # Default ns if the user didn't provide
    if args.n_list:
        n_values = args.n_list
    else:
        if args.algorithm == "naive":
            n_values = [4, 5, 6, 7]
        elif args.algorithm == "optimized":
            n_values = [6, 7, 8, 9, 10]
        else:
            n_values = [10, 11, 12, 13]

    m = Measurement(args.algorithm)
    m.run_experiment(n_values, trials=args.trials)
