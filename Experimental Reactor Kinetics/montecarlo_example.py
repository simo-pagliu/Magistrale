"""
Simple example of monte carlo simulation to estimate the value of pi
With evaluation of the error
"""
# import
import random
import numpy as np

# Initialize
runs = int(1e3)
is_inside = np.zeros(runs)

estimations = int(1e3)
pi_estimates = np.zeros(estimations)

for j in range(estimations):
    # generate random points
    points = np.random.rand(runs, 2)

    # calculate the distance from the origin
    distances = np.sum(points**2, axis=1)

    # check if the points are inside the circle
    is_inside = distances <= 1

    # calculate the ratio of points inside the circle
    ratio = sum(is_inside) / runs # this shoulbe be the area on a quarter of the circle
    # A = pi * r^2, r = 1, so A = pi
    pi_estimates[j] = ratio * 4

# Final estimate of pi
pi_final = np.mean(pi_estimates)

# Evaluate the error
std = np.sqrt(
    1 / estimations *
    1 / (estimations - 1) *
    (
        sum(pi_estimates**2) -
        1 / estimations * sum(pi_estimates)**2
    )
    )

print(f"Estimated value of pi: {pi_final:.5f}")
print(f"Standard Deviation: {std:.5f}")