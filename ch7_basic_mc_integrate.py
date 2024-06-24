import numpy as np
from scipy.stats import expon, gamma

def calculate_integral(distribution, N=10000):
    samples = distribution.rvs(size=N)
    f = samples**2 if distribution.dist.name == 'expon' else samples
    sum_f = np.sum(f)
    sum_f2 = np.sum(f**2)
    fBar = sum_f / N
    f2Bar = sum_f2 / N
    sigma = np.sqrt((f2Bar - fBar**2) / N)
    return fBar, sigma

def main():
    N = 10000

    exp_dist = expon() # Exponential distribution
    fBar, sigma = calculate_integral(exp_dist, N)
    print(f"Integral for exponential distribution is {fBar} +- {sigma}")

    gamma_dist = gamma(a=2) 
    fBar, sigma = calculate_integral(gamma_dist, N)
    print(f"Integral for gamma distribution is {fBar} +- {sigma}")

if __name__ == "__main__":
    main()

