import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def f(x, phi):
    return 1 / (2 - x) + (2 - x) - 2.0 * (1 - x**2) * (np.cos(phi)**2)

MAXTHROW = 2.0
num_samples = 1000000

# Random sample generation
np.random.seed(100)
rx = np.random.uniform(-1.0, 1.0, num_samples)
rphi = np.random.uniform(0.0, 2 * np.pi, num_samples)
ry = np.random.uniform(0.0, MAXTHROW, num_samples)

valid_indices = ry < f(rx, rphi)
filtered_rx = rx[valid_indices]
filtered_rphi = rphi[valid_indices]

hist, xedges, yedges = np.histogram2d(filtered_rx, filtered_rphi, bins=[25, 25], range=[[-1.0, 1.0], [0, 2 * np.pi]])

fig, ax = plt.subplots()
X, Y = np.meshgrid(xedges, yedges)
pcm = ax.pcolormesh(X, Y, hist.T, norm=LogNorm(), cmap='Greys', edgecolor='black', linewidth=0.5)

ax.set_xlabel(r'$x = \cos(\theta)$', fontsize=16, family='sans-serif')
ax.set_ylabel(r'$\phi$', fontsize=16, family='sans-serif')
ax.set_title('X vs PHI', fontsize=16, family='sans-serif')

ax.set_aspect('auto')
plt.colorbar(pcm, ax=ax, extend='max')
plt.grid(False)

plt.show()

