import time
import matplotlib.pyplot as plt
from solution import generate_tricky_graph, hamiltonian_optimized
import numpy as np

def measure_optimized_runtime(n_values, rounds=20, output_png="optimized_plot.png"):
    avg_times = []

    for n in n_values:
        print(f"Measuring n = {n} ...")

        times = []

        for _ in range(rounds):
            # Graph generation — NOT counted
            graph, start, end = generate_tricky_graph(n)

            # Measure only the algorithm itself
            t0 = time.perf_counter()
            hamiltonian_optimized(graph, start, end)
            t1 = time.perf_counter()

            times.append(t1 - t0)

        avg = np.mean(times)
        avg_times.append(avg)
        print(f"  Avg time = {avg:.6f} sec")

    # Plot
    plt.figure(figsize=(9,6))
    plt.plot(n_values, avg_times, marker='o', linewidth=2)
    plt.xlabel("n (subgraph size)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Optimized Algorithm: n vs Execution Time")
    plt.grid(True)

    # Label each point
    for i, t in zip(n_values, avg_times):
        plt.text(i, t, f"{t:.4f}", fontsize=9, ha='center', va='bottom')

    # Save as PNG
    plt.savefig(output_png, dpi=300)
    print(f"\nPlot saved as {output_png}")

    plt.show()

    return avg_times


if __name__ == "__main__":
    # n ≥ 4 , 10 farklı n değeri
    n_values = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    measure_optimized_runtime(n_values)
