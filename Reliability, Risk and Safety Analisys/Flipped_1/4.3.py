import numpy as np
import math
import matplotlib.pyplot as plt

def binomial(n, p):
    x = np.arange(0, n+1)
    y = np.zeros(n+1)
    for k in range(n+1):
        y[k] = math.comb(n, k) * p**k * (1-p)**(n-k)
    return x, y

n = 5  # number of LEDs
p = 0.7  # probability of be working after 1 year

x, y = binomial(n, p)

#compute the mean and the variance
mean = np.sum(x*y)
variance = np.sum((x-mean)**2*y)
#compute the standard deviation
std_dev = np.sqrt(variance)

print('Mean:', mean)
print('Variance:', variance)
print('Standard deviation:', std_dev)


#plot the probability distribution
plt.plot(x, y, 'bo-')
plt.xlabel('LEDs working after 1 year')
plt.ylabel('Probability')
plt.title('Binomial Probability Distribution')
plt.grid(True)
plt.show()

#define the cumulative distribution function
def binomial_cdf(n, p):
    x, y = binomial(n, p)
    y_cdf = np.cumsum(y)
    return x, y_cdf

#plot the cumulative distribution function
x, y_cdf = binomial_cdf(n, p)
plt.plot(x, y_cdf, 'bo-')
plt.xlabel('LEDs working after 1 year')
plt.ylabel('Probability')
plt.title('Binomial Cumulative Distribution')
plt.grid(True)
plt.show()


