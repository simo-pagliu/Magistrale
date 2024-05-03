import numpy as np
import matplotlib.pyplot as plt
#########################################
# Exercise 1 - part 1
# This script generates samples from a Weibull distribution and estimates the probability density function
# using a histogram. The analytical probability density function is also plotted for comparison.
# It's more of a demonstration of how to estimate the pdf of a distribution using samples.
#########################################

# Weibull parameters
tau = 1.0
beta = 1.5

#Sample N values from the Weibull distribution
steps = 4000  # number of samples
samples = []

# Generate samples using the inverse transform method
rand = np.random.rand(steps)
samples = (-np.log(1 - rand))**(1/beta)*tau

# Time discretization for the histogram
t_step = 0.1
t = np.arange(0, 10, t_step)

# Estimate the probability density function
counts, _ = np.histogram(samples, bins=len(t), range=(0, 10)) # histogram of the samples, counting how many samples fall in each bin
pdf_est = counts / (steps * (t[1] - t[0])) # estimation of the probability density function

# Analytical probability density function
pdf = (beta / tau) * (t / tau)**(beta - 1) * np.exp(-(t / tau)**beta)

# plot the pdf
plt.figure()
plt.plot(t, pdf, label='True PDF')
plt.plot(t, pdf_est, label='Estimated PDF', marker='*', linestyle='--')
plt.title("Weibull Distribution")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Probability Density")
plt.show()

#########################################
# Exercise 1 - part 2
# In this part, we estimate G_n = integral of t*g(t)
# and its variance
#########################################

#Sample N values from the Weibull distribution
steps = 4000  # number of samples
rand = np.random.rand(steps) # Generate random values
# rand = rand here it is not necessary to use the inverse transform method since the first function is f(t) = t
samples = (-np.log(1 - rand))**(1/beta)*tau # samples from the Weibull distribution - inverse transform method

# Estimate the integral of t*g(t)
G_n = np.mean(samples) # estimate of the integral of t*g(t)

# Estimate the variance of the integral of t*g(t)
var_G_n = np.var(samples) / steps # estimate of the variance of the integral of t*g(t)
var_G_n_MC = (sum(samples**2) / steps - G_n**2) / steps # estimate of the variance of the integral of t*g(t) using the Monte Carlo method

print('Estimate of the integral of t*g(t):', G_n)
print('Estimate of the variance of the integral of t*g(t):', var_G_n)
print('Estimate of the variance of the integral of t*g(t) using the Monte Carlo method:', var_G_n_MC)