import numpy as np
import matplotlib.pyplot as plt


# DATA
L = 0.5  # Length of the rod (m)
k = 1000  # Thermal conductivity (W/m-K)
A = 0.1  # Cross-sectional area (m^2)
T_A = 500  # Temperature at the left boundary (°C)
T_B = 100  # Temperature at the right boundary (°C)
n = 5 # Number of nodes (excluding boundaries)

# Discretization
dx = L / (n)  # Spacing between nodes
x = np.linspace(0 + dx/2, L - dx/2, n)  # Positions along the rod

# Initialization of the Matrix and the right-hand side vector
K = np.zeros((n, n))
b = np.zeros(n)

# Define the costant
a = k * A / dx

# Filling the coefficient matrix and the right-hand side vector
for i in range(1, n-1):
    K[i, i-1] = - a
    K[i, i] = 2 * a
    K[i, i+1] = - a

# Start boundary condition
K[0, 0] = 3 * a  
K[0, 1] = - a
b[0] = T_A * 2 * a
# End boundary condition
K[-1, -1] = 3 * a
K[-1, -2] = - a
b[-1] = T_B * 2 * a

# Solve for temperatures
T = np.linalg.solve(K, b)
T = [T_A] + list(T) + [T_B]
x = [0] + list(x) + [L]

# Plot the results
plt.figure(figsize=(8, 5))
plt.plot(x, T, 'o-', label='Temperature distribution')
plt.title("Temperature Distribution in a 1D Rod")
plt.xlabel("Position along the rod (m)")
plt.ylabel("Temperature (°C)")
plt.grid()
plt.legend()
plt.show()