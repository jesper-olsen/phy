#PERC03: plots the distribution of cluster sizes for a one-dimensional lattice, comparing results from simulation with the theoretical curve. 


import numpy as np
import matplotlib.pyplot as plt
import sys
import random

def generate_clusters(L, p):
    clusters = []
    current_cluster_size = 0
    for i in range(L):
        if random.random() < p:
            current_cluster_size += 1
        else:
            if current_cluster_size > 0:
                clusters.append(current_cluster_size)
                current_cluster_size = 0
    if current_cluster_size > 0:
        clusters.append(current_cluster_size)
    return clusters

def plot_clusters(clusters, L, p):
    cluster_sizes = np.array(clusters)
    hist, bin_edges = np.histogram(cluster_sizes, bins=100, range=(1, 100), density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    plt.bar(bin_centers, hist, width=bin_centers[1] - bin_centers[0], align='center', label='Cluster size distribution')

    s = np.arange(1, 101)
    theoretical_distribution = (p ** s) * ((1 - p) ** 2)
    plt.plot(s, theoretical_distribution, 'r-', linewidth=3, label='Theoretical distribution')

    plt.title(f'1-dimensional lattice L={L}, p={p}')
    plt.xlabel('Cluster size s')
    plt.ylabel('n_s')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    L = 10000
    p = 0.5

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith("L="):
                L = int(arg.split("=")[1])
            elif arg.startswith("p="):
                p = float(arg.split("=")[1])

    clusters = generate_clusters(L, p)
    plot_clusters(clusters, L, p)

