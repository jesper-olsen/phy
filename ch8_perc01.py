# A simulation of a percolating system.

import numpy as np
from typing import Generator, Tuple, Any    
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from itertools import product
import sys

def neighbours(grid: np.typing.NDArray[Any], xy: (int,int)) -> Generator[Tuple[int, int], None, None]:
    """ neghbours: left-right, up-down  """
    N1, N2 = grid.shape
    g=((di, dj) for (di,dj) in product([-1, 0, 1], repeat=2))
    g=((di,dj) for (di,dj) in g if (di!=0 or dj!=0) and (di==0 or dj==0)) # left-right or up-down
    g=((xy[0]+di,xy[1]+dj) for (di,dj) in g)
    g=((ni,nj) for (ni,nj) in g if 0<=ni<N1 and 0<=nj<N2)
    g=(xy for xy in g if grid[xy]!=0) # occupied neighbours
    yield from g

def percolates(cluster: set, grid_size: int) -> bool:
    """spans the grid top to bottom"""
    return min([xy[0] for xy in cluster]) == 0 and \
           max([xy[0] for xy in cluster]) == grid_size-1

def cluster_index(clusters: list, xy: int) -> int:
    """index of cluster xy belongs to"""
    for i, cluster in enumerate(clusters):
        if xy in cluster:
            return i
    return len(clusters)

def percolation_sim(N: int = 20, P: float = 0.6) -> (np.typing.NDArray[Any], list):
    grid = np.random.binomial(1, P, (N, N)) # Generate the configuration
    clusters = []
    for i, j in ((i,j) for (i,j) in  product(range(N), range(N)) if grid[i,j]>0):
        p0 = (i, j)
        i0 = cluster_index(clusters, p0)
        for p1 in neighbours(grid, p0):
            i1 = cluster_index(clusters, p1)
            if i0 == len(clusters) and i1 == len(clusters):
                clusters += [ set([p0,p1]) ]
                i0 = cluster_index(clusters, p0)
            elif i0 != i1 and i0 == len(clusters):
                clusters[i1].add(p0)
            elif i0 != i1 and i1 == len(clusters):
                clusters[i0].add(p1)
            elif i0 != i1:
                clusters[i0].update(clusters[i1]) 
                del clusters[i1]
                i0 = cluster_index(clusters, p0)

    return grid, clusters

def perc01():
    N=20  # Lattice size (square)
    P=0.5 # Site occupation probability

    fig, ax = plt.subplots()
    while True:
        grid, clusters = percolation_sim(N, P)
        #single out percolating clusters
        n_percolating=0
        for i,c in enumerate(clusters):
            if percolates(c, N):
                n_percolating+=1
            for xy in c:
                grid[xy]=i+1
        print(f"#clusters: {len(clusters)}; #percolating: {n_percolating}")
        #print(grid)

        bcolours=['white']
        ecolours=['lightblue', 'pink', 'lightgreen', 'yellow', 'cyan', 'magenta',
                 'black', 'gray', 'orange', 'red', 'blue', 'brown', 'purple', 'darkblue', 
                 'green', 'darkgreen', 'lightgray', 'darkgray', 'gold']
        colours = bcolours + ecolours
        n_clusters = len(set(grid.flatten())) 
        if n_clusters > len(colours):
            colours += [ecolours[i%len(ecolours)] for i in range(n_clusters-len(ecolours))]
        cmap = mcolors.ListedColormap(colours)
        bounds = list(range(len(colours) + 1))
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        ax.clear()
        ax.imshow(grid, cmap=cmap, norm=norm)
        ax.set_title('Percolation grid', fontsize=16, color='lightblue')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.draw()
        plt.pause(1)
        s=input("Press Enter to continue/q to quit...")
        if s.strip()=='q': 
            sys.exit(1)
        else:
            sys.stdout.write("\033[F")  # Move the cursor up one line
            sys.stdout.write("\033[K")  # Clear the line
     
        ax.clear()

def perc02():
    """ Plot probability of percolation vs site occupation probability for a 2x2 lattice
    """
    NRUNS = 1000
    N = 2
    NDIV = 25

    results = []
    for P in np.linspace(0, 1, NDIV):
        nPERC = 0
        for _ in range(NRUNS):
            grid, clusters = percolation_sim(N, P)
            for i,c in enumerate(clusters):
                if percolates(c, N): nPERC+=1

        prob = nPERC / NRUNS
        results.append((P, prob, np.sqrt(prob * (1 - prob) / NRUNS)))

    ps, probs, errors = zip(*results)
    plt.errorbar(ps, probs, yerr=errors, fmt='o', label='Numerical calculation')

    if N == 2:
        exact_p = np.linspace(0, 1, 100)
        exact_prob = exact_p ** 2 * (2 - exact_p ** 2)
        plt.plot(exact_p, exact_prob, label='Exact solution')

    plt.xlabel('Site occupation probability')
    plt.ylabel('P(p, 2)')
    plt.title('Percolation probability')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    perc01()
    #perc02()
