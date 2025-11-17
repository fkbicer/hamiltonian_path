import random


class GraphConstructor:
    def __init__(self, seed=None):
        """
        Initialize the constructor.

        Parameters
        ----------
        seed : int or None
            Random seed for reproducibility.
        """
        if seed is not None:
            random.seed(seed)

    def __add_connected_subgraph(self, graph, vertices):
        """
        Creates a connected subgraph over 'vertices' by:
        1) Building a random spanning path (ensures connectivity)
        2) Adding random extra edges with p = 1/2
        """
        L = vertices[:]                 # copy
        random.shuffle(L)               # random spanning path

        # Step 1: spanning path
        for k in range(len(L) - 1):
            u, v = L[k], L[k + 1]
            graph[u][v] = graph[v][u] = 1

        # Step 2: extra edges (p = 1/2)
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u, v = vertices[i], vertices[j]
                if graph[u][v] == 0 and random.random() < 0.5:
                    graph[u][v] = graph[v][u] = 1

    # PUBLIC API
    def generate_tricky_graph(self, n):
        """
        Generate the 3-subgraph tricky graph used in CMPE300 project.

        Parameters
        ----------
        n : int
            Each subgraph size → total graph has 3n vertices.

        Returns
        -------
        graph : list[list[int]]
            Adjacency matrix (3n x 3n)

        start : int
            Random start vertex

        end : int
            Random end vertex, end != start
        """
        N = 3 * n

        # Random start & end
        start = random.randint(0, N - 1)
        end = random.randint(0, N - 1)
        while end == start:
            end = random.randint(0, N - 1)

        # Empty adjacency matrix
        graph = [[0] * N for _ in range(N)]

        # Define the 3 subgraphs A, B, C
        A = list(range(0, n))
        B = list(range(n, 2 * n))
        C = list(range(2 * n, 3 * n))

        # Add connected subgraphs
        self.__add_connected_subgraph(graph, A)
        self.__add_connected_subgraph(graph, B)
        self.__add_connected_subgraph(graph, C)

        # Random permutation of vertex labels
        perm = list(range(N))
        random.shuffle(perm)
        inv = [0] * N
        for i, p in enumerate(perm):
            inv[p] = i

        # Permute adjacency matrix
        permuted = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                permuted[i][j] = graph[perm[i]][perm[j]]

        # Update start & end after permutation
        start = inv[start]
        end = inv[end]

        return permuted, start, end
