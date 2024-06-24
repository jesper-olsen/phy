import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 3/4 * (1 - x**2)

np.random.seed(100)
rx = np.random.uniform(-1, 1, 1000000)
ry = np.random.uniform(0, 0.75, 1000000)
hx = rx[ry < f(rx)]

plt.hist(hx, bins=100, range=(-2.0, 2.0), density=True, alpha=0.75, edgecolor='black')
plt.title('Histogram of X', fontsize=16, family='sans-serif')
plt.xlabel('x', fontsize=16, family='sans-serif')
plt.ylabel(r'$\rho(x)$', fontsize=16, family='sans-serif')
plt.grid(False)
plt.show()

