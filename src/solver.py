"""
Hamiltonian Path Solver Class
Contains: naive, optimized, and DP (bonus) algorithms.
"""

from itertools import combinations
from collections import deque
from src.utils import hamiltonian_check, all_permutations


class Solver:
    def __init__(self, graph, start, end):
        self.graph = graph
        self.start = start
        self.end = end
        self.N = len(graph)

    # 1) NAIVE ALGORITHM
    def __naive(self):
        n = self.N // 3
        V = list(range(self.N))
        others = [v for v in V if v not in (self.start, self.end)]
        # choose n-2 vertices from V \ {start, end} (combinations)
        for rest in combinations(others, n - 2):
            L = [self.start, *rest, self.end]
            H = [[self.graph[L[i]][L[j]] for j in range(n)] for i in range(n)]
            # start = 0, end = n-1
            if all_permutations(H, 0, n - 1):
                return True

        return False

    # 2) OPTIMIZED ALGORITHM
    def __optimized(self):
        visited = [False] * self.N
        component = []
        # find connected component using BFS
        queue = deque([self.start])
        visited[self.start] = True
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in range(self.N):
                if self.graph[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    queue.append(v)
        # if end not in same component -> return False
        if self.end not in component:
            return False

        m = len(component)
        H = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                H[i][j] = self.graph[component[i]][component[j]]
        # reindex start and end relative to this component
        s = component.index(self.start)
        t = component.index(self.end)

        return all_permutations(H, s, t)

    # 3) BONUS ALGORITHM (BITMASK DP)
    def __bonus(self):
        visited = [False] * self.N
        component = []

        queue = deque([self.start])
        visited[self.start] = True
        while queue:
            u = queue.popleft()
            component.append(u)
            for v in range(self.N):
                if self.graph[u][v] == 1 and not visited[v]:
                    visited[v] = True
                    queue.append(v)

        if self.end not in component:
            return False

        m = len(component)
        H = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                H[i][j] = self.graph[component[i]][component[j]]

        s = component.index(self.start)
        t = component.index(self.end)
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

    # UNIVERSAL SOLVE METHOD
    def execute(self, method="bonus"):
        if method == "naive":
            return self.__naive()
        elif method == "optimized":
            return self.__optimized()
        elif method == "bonus":
            return self.__bonus()
        else:
            raise ValueError("Unknown method: choose naive / optimized / bonus")
