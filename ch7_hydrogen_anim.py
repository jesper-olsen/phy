import numpy as np
import pyvista as pv
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
        r[1] = v_prop[2] / r[0] if r[0] != 0 else 0
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
        # Simplified model for hydrogen wavefunction
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

    v_state = np.array([30.0, 0.0, 0.0])
    v_prob = 0.0

    chain = HydrogenAtomMarkovChain(N, L, M, fSigma * N)

    points = []
    for _ in range(NPOINTS):
        v_state, v_prob = chain.move(v_state, v_prob)
        points.append(v_state)

    points = np.array(points)

    # Visualization using pyvista
    cloud = pv.PolyData(points)
    plotter = pv.Plotter()
    plotter.add_mesh(cloud, color="red", point_size=5.0, render_points_as_spheres=True)
    
    # Add a cube for reference
    plotter.add_mesh(pv.Cube(center=(0, 0, 0), x_length=30, y_length=30, z_length=30), color="blue", style='wireframe')

    plotter.show_grid()
    plotter.show()

if __name__ == "__main__":
    main()
