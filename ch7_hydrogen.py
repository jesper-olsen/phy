import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

class HydrogenAtomMarkovChain:
    def __init__(self, n, l, m, sigma=1.0):
        self.psi = Psi2Hydrogen(n, l, m)
        self.engine = np.random.default_rng()
        self.gauss = lambda: self.engine.normal(0, sigma)

    def move(self, v, prob=0.0):
        v_prop = v + np.array([self.gauss(), self.gauss(), self.gauss()])
        
        r = np.zeros(3)
        r[0] = np.linalg.norm(v_prop)
        r[1] = v_prop[2] / r[0]
        r[2] = np.arctan2(v_prop[1], v_prop[0])
        
        new_prob = self.psi(r)
        if new_prob > prob:
            return v_prop, new_prob
        else:
            if self.engine.uniform(0, 1) < new_prob / prob:
                return v_prop, new_prob
            else:
                return v, prob

class Psi2Hydrogen:
    def __init__(self, n, l, m):
        self.n = n
        self.l = l
        self.m = m

    def __call__(self, r):
        return np.exp(-r[0]) * (r[0] ** self.l) * np.abs(np.sin(r[1]) ** self.m)

def main():
    parser = argparse.ArgumentParser(description="Hydrogen atom Markov chain visualization")
    parser.add_argument('--NPOINTS', type=int, default=10000, help='Number of points in the Markov Chain')
    parser.add_argument('--N', type=int, default=1, help='Principal Quantum Number')
    parser.add_argument('--L', type=int, default=0, help='Angular Momentum Quantum Number')
    parser.add_argument('--M', type=int, default=0, help='Magnetic Quantum Number')
    parser.add_argument('--fSigma', type=float, default=1.0, help='Under/over scale the proposal distribution')
    args = parser.parse_args()

    NPOINTS = args.NPOINTS
    N = args.N
    L = args.L
    M = args.M
    fSigma = args.fSigma
    
    v = np.zeros(3)
    rebound_collection = []
    chain = HydrogenAtomMarkovChain(N, L, M, fSigma * N)
    prob = 0.0

    for _ in range(NPOINTS):
        rebound_collection.append(v)
        v, prob = chain.move(v, prob)
    
    rebound_collection = np.array(rebound_collection)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(rebound_collection[:, 0], rebound_collection[:, 1], rebound_collection[:, 2], c='k', marker='o')
    ax.set_title(f'Hydrogen {N} {L} {M}')
    plt.show()

if __name__ == "__main__":
    main()

