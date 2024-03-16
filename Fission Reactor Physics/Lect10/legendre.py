#legendre polynomials
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre
x = np.linspace(-1, 1, 100)
for i in range(5):
    plt.plot(x, legendre(i)(x), label=f'n={i}')
plt.legend()
plt.show()

#