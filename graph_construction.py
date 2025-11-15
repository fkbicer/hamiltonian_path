import random
import matplotlib.pyplot as plt
import networkx as nx
import itertools
from collections import deque
# ------------------------------
# Graph construction (spec §2.1)
# ------------------------------
def add_connected_subgraph(graph, vertices):
    L = vertices[:]
    random.shuffle(L)  # Step 1: random spanning path to ensure connectivity
    for k in range(len(L) - 1):
        u, v = L[k], L[k + 1]
        graph[u][v] = graph[v][u] = 1
    # Add extra random edges with p=1/2 among remaining pairs
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            u, v = vertices[i], vertices[j]
            if graph[u][v] == 0 and random.random() < 0.5:
                graph[u][v] = graph[v][u] = 1

    

def generate_tricky_graph(n):
    N = 3 * n
    start = random.randint(0, N - 1)
    while True:
        end = random.randint(0, N - 1)
        if end != start:
            break

    graph = [[0] * N for _ in range(N)]

    A = list(range(0, n))
    B = list(range(n, 2 * n))
    C = list(range(2 * n, 3 * n))

    add_connected_subgraph(graph, A)
    add_connected_subgraph(graph, B)
    add_connected_subgraph(graph, C)

    # Hide structure by permuting vertex labels; remap start/end accordingly
    perm = list(range(N))
    random.shuffle(perm)
    inv = [0] * N
    for i, p in enumerate(perm):
        inv[p] = i
    
    permuted = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            permuted[i][j] = graph[perm[i]][perm[j]]
    graph = permuted
    start = inv[start]
    end = inv[end]

    return graph, start, end




def draw_graph(graph, start=None, end=None):
    N = len(graph)
    G = nx.Graph()

    # adjacency matrix'ten kenarları ekle
    for i in range(N):
        for j in range(i + 1, N):
            if graph[i][j] == 1:
                G.add_edge(i, j)

    # çizim renkleri (start ve end düğümlerini vurgula)
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append("limegreen")  # yeşil = başlangıç
        elif node == end:
            node_colors.append("red")        # kırmızı = bitiş
        else:
            node_colors.append("lightblue")  # normal düğümler

    # grafı çiz
    plt.figure(figsize=(6, 4))
    nx.draw(G, with_labels=True, node_color=node_colors, 
            font_weight="bold", node_size=700)
    plt.show()

def hamiltonian_check(H, perm):
    n = len(H)
    for i in range(n - 1):
        if H[perm[i]][perm[i + 1]] == 0:
            return False  # edge missing
    return True  # all consecutive pairs are adjacent

# ---------------------------------
# Algorithm 4: AllPermutations
# ---------------------------------
def all_permutations(H, s, t):
    n = len(H)
    # generate all permutations with fixed start and end
    nodes = [i for i in range(n) if i not in (s, t)]
    for mid in itertools.permutations(nodes):
        perm = (s,) + mid + (t,)
        if hamiltonian_check(H, perm):
            return True
    return False

# ---------------------------------
# Algorithm 3: Hamiltonian*Naive
# ---------------------------------
def hamiltonian_naive(graph, start, end):
    from itertools import combinations
    N = len(graph)
    n = N // 3
    V = list(range(N))

    # start ve end dışındakilerden n-2 seç
    others = [v for v in V if v not in (start, end)]
    for rest in combinations(others, n - 2):
        # L'yi sabit bir sırayla kur: start ... end
        L = [start, *rest, end]

        # indüklenen alt-graf H (n x n)
        H = [[graph[L[i]][L[j]] for j in range(n)] for i in range(n)]


        # start = 0, end = n-1 oldu
        if all_permutations(H, 0, n - 1):
            return True
    return False

def hamiltonian_optimized(graph, start, end):
    """
    Optimized Hamiltonian* Path algorithm (correct version)
    - Detects the connected component containing 'start'
    - If 'end' is in that component, searches only there
    - Otherwise immediately returns False
    """
    N = len(graph)

    visited = [False] * N
    component = []

    queue = deque([start])
    visited[start] = True
    while queue:
        u = queue.popleft()
        component.append(u)
        for v in range(N):
            if graph[u][v] == 1 and not visited[v]:
                visited[v] = True
                queue.append(v)

    # Step 2: if end is not in the same connected component, return False
    if end not in component:
        return False

    # Step 3: build induced subgraph H for that component
    m = len(component)
    H = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            H[i][j] = graph[component[i]][component[j]]

    # Step 4: reindex start and end relative to this component
    s = component.index(start)
    t = component.index(end)

    # Step 5: use existing all_permutations()
    return all_permutations(H, s, t)

from collections import deque

def hamiltonian_bonus(graph, start, end):
    """
    Bonus algorithm: BFS + Bitmask DP
    ---------------------------------
    1. BFS to isolate connected component of 'start'
    2. If 'end' not in same component -> immediately False
    3. Run Hamiltonian Path bitmask DP only within that component
    """

    N = len(graph)

    # --- Step 1: find connected component using BFS ---
    visited = [False] * N
    component = []

    queue = deque([start])
    visited[start] = True
    while queue:
        u = queue.popleft()
        component.append(u)
        for v in range(N):
            if graph[u][v] == 1 and not visited[v]:
                visited[v] = True
                queue.append(v)

    # --- Step 2: if end not in same component, no path ---
    if end not in component:
        return False

    # --- Step 3: build induced subgraph H for that component ---
    m = len(component)
    H = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            H[i][j] = graph[component[i]][component[j]]

    # --- Step 4: re-index start and end relative to this subgraph ---
    s = component.index(start)
    t = component.index(end)

    # --- Step 5: Bitmask DP on the smaller subgraph ---
    dp = [[False] * m for _ in range(1 << m)]
    dp[1 << s][s] = True

    for mask in range(1 << m):
        for j in range(m):
            if dp[mask][j]:
                for k in range(m):
                    if H[j][k] == 1 and not (mask & (1 << k)):
                        dp[mask | (1 << k)][k] = True

    return dp[(1 << m) - 1][t]



import time

if __name__ == "__main__":
    n = 15  # her alt-graftaki düğüm sayısı (toplam 3n düğüm)
    graph, start, end = generate_tricky_graph(n)
    print(f"Start node: {start}")
    print(f"End node:   {end}")



    start_time = time.perf_counter()
    optimized_result = hamiltonian_optimized(graph, start, end)
    optimized_time = time.perf_counter() - start_time

    print(f"Optimized result: {optimized_result}")

        # ------------------------------
    # Optimize edilmiş algoritmayı test et
    # ------------------------------
    start_time = time.perf_counter()
    bonus_result = hamiltonian_bonus(graph, start, end)
    bonus_time = time.perf_counter() - start_time

    print(f"Bonus result: {bonus_result}")

    # ------------------------------
    # Sonuç karşılaştırması
    # ------------------------------

    # ------------------------------
    # Süre karşılaştırması
    # ------------------------------
    #print(f"Naive:     {naive_time:.8f} sec ({naive_time*1e6:.2f} µs)")
    print(f"Optimized: {optimized_time:.8f} sec ({optimized_time*1e6:.2f} µs)")
    print(f"Bonus:     {bonus_time:.8f} sec ({bonus_time*1e6:.2f} µs)")
    
    """
        if optimized_time > 0:
        print(f"Speed-up:  ~{naive_time / optimized_time:.2f}x faster")
    else:
        print("Speed-up:  ∞ (instantaneous)")



    start_time = time.perf_counter()
    naive_result = hamiltonian_naive(graph, start, end)
    naive_time = time.perf_counter() - start_time

    print(f"Naive result: {naive_result}")
    """

