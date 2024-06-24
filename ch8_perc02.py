import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class Index:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return (self.i, self.j) < (other.i, other.j)

    def neighbors(self, other):
        return (self.i == other.i and abs(self.j - other.j) == 1) or (self.j == other.j and abs(self.i - other.i) == 1)

    def __hash__(self):
        return hash((self.i, self.j))

class Cluster:
    def __init__(self):
        self.indexSet = set()

    def percolates(self, gridSize):
        if self.indexSet:
            return min(idx.i for idx in self.indexSet) == 0 and max(idx.i for idx in self.indexSet) == gridSize - 1
        return False

    def contains(self, index):
        return index in self.indexSet

    def add(self, index):
        self.indexSet.add(index)

    def add_cluster(self, cluster):
        self.indexSet.update(cluster.indexSet)

class ClusterSet:
    def __init__(self):
        self._cluster = []

    def add(self, cluster):
        self._cluster.append(cluster)

    def __getitem__(self, i):
        return self._cluster[i]

    def __delitem__(self, i):
        del self._cluster[i]

    def clusterIndex(self, index):
        for i, cluster in enumerate(self._cluster):
            if cluster.contains(index):
                return i
        return len(self._cluster)

    def size(self):
        return len(self._cluster)

def percolation_simulation(N, NRUNS, NDIV):
    results = []
    for p in np.linspace(0, 1, NDIV):
        nPERC = 0.0
        for _ in range(NRUNS):
            grid = np.random.rand(N, N) < p
            clusterSet = ClusterSet()
            action = True
            while action:
                action = False
                for (i,j) in ((i,j) for i in range(N) for j in range(N)):
                    if grid[i, j]:
                        p0 = Index(i, j)
                        i0 = clusterSet.clusterIndex(p0)
                        for (di,dj) in ((i,j) for i in [-1,0,1] for j in [-1,0,1]):
                            ni, nj = i + di, j + dj
                            if 0 <= ni < N and 0 <= nj < N and grid[ni, nj] and (di, dj) != (0, 0):
                                p1 = Index(ni, nj)
                                i1 = clusterSet.clusterIndex(p1)
                                if i0 == clusterSet.size() and i1 == clusterSet.size():
                                    cluster = Cluster()
                                    cluster.add(p0)
                                    cluster.add(p1)
                                    clusterSet.add(cluster)
                                    i0 = clusterSet.clusterIndex(p0)
                                    action = True
                                elif i0 != i1:
                                    if i0 == clusterSet.size():
                                        clusterSet[i1].add(p0)
                                        action = True
                                    elif i1 == clusterSet.size():
                                        clusterSet[i0].add(p1)
                                        action = True
                                    else:
                                        clusterSet[i0].add_cluster(clusterSet[i1])
                                        del clusterSet[i1]
                                        i0 = clusterSet.clusterIndex(p0)
                                        action = True
            for cluster in clusterSet._cluster:
                if cluster.percolates(N): nPERC += 1
        prob = nPERC / NRUNS
        results.append((p, prob, np.sqrt(prob * (1 - prob) / NRUNS)))
    return results

def plot_results(results, N):
    ps, probs, errors = zip(*results)
    plt.errorbar(ps, probs, yerr=errors, fmt='o', label='Numerical calculation')

    if N == 2:
        exact_p = np.linspace(0, 1, 100)
        exact_prob = exact_p ** 2 * (2 - exact_p ** 2)
        plt.plot(exact_p, exact_prob, label='Exact solution')

    plt.xlabel('p')
    plt.ylabel('P(p, 2)')
    plt.title('Percolation probability')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    import sys
    NRUNS = 1000
    N = 2
    NDIV = 25

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("NRUNS="):
                NRUNS = int(arg.split("=")[1])
            elif arg.startswith("N="):
                N = int(arg.split("=")[1])
            elif arg.startswith("NDIV="):
                NDIV = int(arg.split("=")[1])

    results = percolation_simulation(N, NRUNS, NDIV)
    plot_results(results, N)

