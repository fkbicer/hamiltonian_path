import time
import matplotlib.pyplot as plt
from solution import generate_tricky_graph, hamiltonian_naive

def measure_naive():
    ns = [4, 5, 6, 7, 8]
    avg_times = []

    for n in ns:
        print(f"Running experiments for n = {n} ...")
        run_times = []

        for _ in range(1):
            graph, start, end = generate_tricky_graph(n)

            t0 = time.time()
            hamiltonian_naive(graph, start, end)
            t1 = time.time()

            run_times.append(t1 - t0)

        avg_time = sum(run_times) / len(run_times)
        avg_times.append(avg_time)

        print(f"  Avg time: {avg_time:.6f} sec")

    # ======== PLOT ========
    plt.figure(figsize=(9, 6))
    plt.plot(ns, avg_times, marker='o', linestyle='-', color='blue')

    plt.xticks(ns)
    plt.xlabel("n (subgraph size)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Naive Hamiltonian* Algorithm — n vs execution time")
    plt.grid(True)

    # Add text labels above points
    for x, y in zip(ns, avg_times):
        plt.text(x, y, f"{y:.4f}", fontsize=10, ha='center', va='bottom')

    # ======== SAVE PNG OUTPUT ========
    output_path = "naive_plot.png"
    plt.savefig(output_path, dpi=300)
    print(f"\nSaved plot to: {output_path}\n")

    # Show on screen
    plt.show()

    return ns, avg_times


if __name__ == "__main__":
    measure_naive()
