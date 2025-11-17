import random
import itertools
from collections import deque
from itertools import combinations

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

def hamiltonian_check(H, perm):
    n = len(H)
    for i in range(n - 1):
        if H[perm[i]][perm[i + 1]] == 0:
            return False  # edge missing
    return True  # all consecutive pairs are adjacent

def all_permutations(H, s, t):
    n = len(H)
    # generate all permutations with fixed start and end
    nodes = [i for i in range(n) if i not in (s, t)]
    for mid in itertools.permutations(nodes):
        perm = (s,) + mid + (t,)
        if hamiltonian_check(H, perm):
            return True
    return False

def hamiltonian_naive(graph, start, end):

    N = len(graph)
    n = N // 3
    V = list(range(N))

    # choose n-2 vertices from V \ {start, end}
    others = [v for v in V if v not in (start, end)]
    for rest in combinations(others, n - 2):
        # create L in which start and end are fixed
        L = [start, *rest, end]
        # induced subgraph
        H = [[graph[L[i]][L[j]] for j in range(n)] for i in range(n)]
        # start = 0, end = n-1
        if all_permutations(H, 0, n - 1):
            return True
    return False

def hamiltonian_optimized(graph, start, end):
    N = len(graph)

    visited = [False] * N
    component = []

    # find connected component using BFS
    queue = deque([start])
    visited[start] = True
    while queue:
        u = queue.popleft()
        component.append(u)
        for v in range(N):
            if graph[u][v] == 1 and not visited[v]:
                visited[v] = True
                queue.append(v)

    # if end is not in the same connected component, return False
    if end not in component:
        return False

    # build induced subgraph H for that component
    m = len(component)
    H = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            H[i][j] = graph[component[i]][component[j]]

    # reindex start and end relative to this component
    s = component.index(start)
    t = component.index(end)

    return all_permutations(H, s, t)

def hamiltonian_bonus(graph, start, end):
    N = len(graph)

    # find connected component using BFS
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
    if end not in component:
        return False

    # build induced subgraph H for that component
    m = len(component)
    H = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            H[i][j] = graph[component[i]][component[j]]

    # re-index start and end relative to this subgraph ---
    s = component.index(start)
    t = component.index(end)

    # bitmask DP on the smaller subgraph
    dp = [[False] * m for _ in range(1 << m)]
    dp[1 << s][s] = True

    for mask in range(1 << m):
        for j in range(m):
            if dp[mask][j]:
                for k in range(m):
                    if H[j][k] == 1 and not (mask & (1 << k)):
                        dp[mask | (1 << k)][k] = True

    return dp[(1 << m) - 1][t]