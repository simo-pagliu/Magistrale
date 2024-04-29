import numpy as np
import matplotlib.pyplot as plt

# Constants
l = 0.1  # Decay constant

# Time range, ensuring it starts from 0
t = np.linspace(0, 50, 400)

# Normalized exponential decay calculation
N_normalized = np.exp(-l*t)

# Creating subplots for logarithmic and linear scale representations
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Subplot 1: Logarithmic scale
ax1.plot(t, N_normalized, label='$N/N_0 = e^{-\lambda t}$')
ax1.set_yscale('log')
# Adjust y-axis to start at the smallest non-zero value of N_normalized
ax1.set_ylim(bottom=np.min(N_normalized[N_normalized > 0]))
ax1.set_xlim(left=0)  # x-axis starts from 0
ax1.set_xlabel('Time ($t$)')
ax1.set_ylabel('Normalized Quantity ($N/N_0$)')
ax1.set_title('Normalized Exponential Decay in Logarithmic Scale')
ax1.legend()
ax1.grid(True, which="both", ls="--")

# Subplot 2: Linear scale with y-axis adjustments
ax2.plot(t, N_normalized, label='$N/N_0 = e^{-\lambda t}$')
ax2.set_xlim(left=0)  # x-axis starts from 0
ax2.set_xlabel('Time ($t$)')
ax2.set_ylabel('Normalized Quantity ($N/N_0$)')
ax2.set_title('Normalized Exponential Decay in Linear Scale')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()