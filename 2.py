import math
import numpy as np

print(math.sin(10))

a = np.arange(0,11,1)
print(a[:5])
print(a[::2])
print(a[-1:3])

#plot the function y=x
import matplotlib.pyplot as plt
x = np.linspace(-10,10,100)
y = x
plt.plot(x,y)
plt.show()

array = np.array([1, 4, 5])
print(array)

#plot a hyperbolic sin
x = np.linspace(-10,10,100)
y = np.sinh(x)
plt.plot(x,y)
plt.show()

#plot a hyperbolic cos
x = np.linspace(-10,10,100)
y = np.cosh(x)
plt.plot(x,y)
plt.show()



