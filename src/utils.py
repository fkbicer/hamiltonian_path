import itertools

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