import numpy as np
import matplotlib.pyplot as plt

# DATA
L = 1  # Length of the rod (m)
k = 0.1  # Thermal conductivity (W/m-K)
n = 5 # Number of nodes (excluding boundaries)
u = 0.1  # Velocity of the fluid (m/s)
rho = 1  # Density of the fluid (kg/m^3)
phi_A = 1
phi_B = 0

# Discretization
dx = L / (n)  # Spacing between nodes
x = np.linspace(0 + dx/2, L - dx/2, n)  # Positions along the rod

# Constants
D = k / dx
F = u * rho 
print(f"Peclet number Pe = {F/D}")

# Initialization of the Matrix and the right-hand side vector
K = np.zeros((n, n))
b = np.zeros(n)

# Filling the coefficient matrix and the right-hand side vector
for i in range(1, n-1):
    K[i, i-1] = -(D + F/2)
    K[i, i] = 2 * D
    K[i, i+1] = -(D - F/2)
# Start boundary condition
K[0, 0] = 3*D + F/2
K[0, 1] = -(D - F/2)
b[0] = (2*D + F) * phi_A
# End boundary condition
K[-1, -1] = 3*D - F/2
K[-1, -2] = -(D + F/2)
b[-1] = (2*D - F) * phi_B

# Print the matrix and the right-hand side vector
print(K)
print(b)

# Solve for temperatures
phi = np.linalg.solve(K, b)
phi = [phi_A] + list(phi) + [phi_B]
x = [0] + list(x) + [L]

# Plot this second result
plt.figure(figsize=(8, 5))
plt.plot(x, phi, 'o-', label='Concentration distribution')
plt.title("Concentration Distribution in a 1D Rod")
plt.xlabel("Position along the rod (m)")
plt.ylabel("Concentration")
plt.grid()
plt.legend()
plt.show()