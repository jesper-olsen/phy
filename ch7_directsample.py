# Demo: Direct sampling method, otherwise known as the transformation method.
# 3 Examples of distributions

import numpy as np
import matplotlib.pyplot as plt

# from scipy.special import theta
from scipy.stats import expon, cauchy
import argparse
import sys

def theta(x):
    return np.heaviside(x, 0)

parser = argparse.ArgumentParser(description="Plot different distributions.")
parser.add_argument(
    "-ex",
    type=int,
    choices=[1, 2, 3],
    required=True,
    help="Example number (1: Exponential, 2: Cauchy, 3: Triangular)",
)
args = parser.parse_args()
EX = args.ex

Tau = 3.0
N = 100000

np.random.seed()
u = np.random.uniform(0.0, 1.0, N) if EX != 3 else np.random.uniform(-1.0, 1.0, N)

# Define the distributions and their sampling equations
match EX:
    case 1:
        f = lambda x: (1 / Tau) * np.exp(-x / Tau)
        S = lambda x: -Tau * np.log(1 - x)
        title = "Exponential distribution"
        minX = 0
    case 2:
        f = lambda x: 1 / (np.pi * (1 + x**2))
        S = lambda x: np.tan(np.pi * (x - 0.5))
        title = "Cauchy/Breit-Wigner distribution"
        minX = -10
    case _:
        S30 = lambda x: np.sqrt(np.abs(4 * x)) - 2
        f = lambda x: theta(2 - np.abs(x)) * (
            theta(-x) * 0.25 * (2 + x) + theta(x) * 0.25 * (2 - x)
        )
        S = lambda x: theta(x) * S30(x) - theta(-x) * S30(-x)
        title = "Triangular distribution"
        minX = -10

samples = S(u)  # Sample from the distribution

hist, bins = np.histogram(samples, bins=100, range=(minX, 10), density=True)
bin_centers = (bins[:-1] + bins[1:]) / 2

plt.hist(
    samples,
    bins=100,
    range=(minX, 10),
    density=True,
    alpha=0.75,
    edgecolor="black",
    label="Histogram",
)
x = np.linspace(minX, 10, 1000)
plt.plot(x, f(x), "r-", linewidth=2, label="PDF")

plt.title(title, fontsize=16, family="sans-serif")
plt.xlabel("x", fontsize=16, family="sans-serif")
plt.ylabel(r"$\rho(x)$", fontsize=16, family="sans-serif")
plt.legend()

plt.show()
