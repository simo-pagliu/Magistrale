import numpy as np
import math
import matplotlib.pyplot as plt

#define an array
x = np.array([1, 1, 1, 3, 3, 3])

#divide each element of the array by 12
x = x/12
#multiply each element of the array by values from 0 to 5


#plot x over y
plt.plot(np.arange(0, 6), x, 'bo-')
plt.xlabel('#PUMPS')
plt.ylabel('P(working)')
#only show ticks on the y axis at 1/3 and 1/12
plt.yticks([1/12, 3/12])
#show y axis ticks as fractions
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: '1/{:d}'.format(int(1/x))))
plt.title('Probability Distribution')
plt.grid(True)
plt.show()

#calculate the mean
y = np.array([9/12, 1, 15/12, 0, 1/12, 1/6])
print(y)
mean = np.sum(y)
#calculate the variance
variance = np.sum(x*(np.arange(0, 6)-mean)**2)
#calculate the standard deviation
std_dev = math.sqrt(variance)

print('Mean:', mean)
print('Standard deviation:', std_dev)

#calculate the probability of more then 2 events given as a probability distribution the array x
prob = np.sum(x[3:6])
print('Probability:', prob)

