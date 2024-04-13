import numpy as np
#########################################
# Exercise 3
#########################################
x = np.array([1, 2, 3, 4]) # Define the values of the random variable X

pdf = np.array([1/10, 2/10, 3/10, 4/10]) # Define the probability distribution f_X(x)
cdf = np.cumsum(pdf) # Compute the cumulative distribution function F_X(x)

picks = 1000  # Define the number of samples to draw
samples = np.zeros(picks) # Initialize an array to hold the sampled values

for i in range(picks):
    rand = np.random.rand() # Generate a random number between 0 and 1
    Index = np.searchsorted(cdf, rand)  # and find the smallest value of X for which F(X) >= rho
    samples[i] = x[Index] 

# Estimate the observed probabilities
p_obs = np.zeros(len(x))
for i in range(len(x)):
    p_obs[i] = np.sum(samples == x[i]) / picks

# Print the observed probabilities
print('Observed probabilities:')
print(p_obs)
print('Original probabilities:')
print(pdf)
