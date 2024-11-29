# load XY_convert.py that is up one level, in scripts folder
import sys
sys.path.append('./CFD for Nuclear Engineering/scripts/')
from XY_convert import *
import numpy as np

# Some general data from the CFD simulation
v_bulk = 0.292
width = 2
rho = 1.225  # kg/m^3, air density at sea level

# Load CSV file
# Normalized cross-stream velocity data
# Normalized to the avgerage velocity
# X data is coordinate over the half-length of the channel (-1 to 1)
# First at -0.5 from the center (x_05 and y_05)
# Second at -0.75 from the center (x_075 and y_075)
data = np.genfromtxt('CFD for Nuclear Engineering/Lab_07-NLEVM/plot-data_minus05.csv', delimiter=',', skip_header=1)
x_05, y_05 = data[:, 0], data[:, 1]
# CFD data from Fluent
x_05_fluent, y_05_fluent = load_xy_data('CFD for Nuclear Engineering/Lab_07-NLEVM/crossstream-velocity-05')
# take half of the data
# x_05_fluent = x_05_fluent[:len(x_05_fluent)//2]
# y_05_fluent = y_05_fluent[:len(y_05_fluent)//2]
# Normalize
x_05_fluent = (-np.array(x_05_fluent) + width) / width # Normalize to the half-width of the channel
y_05_fluent = np.array(y_05_fluent) / v_bulk # Normalize to the bulk velocity

data = np.genfromtxt('CFD for Nuclear Engineering/Lab_07-NLEVM/plot-data_minus075.csv', delimiter=',', skip_header=1)
x_075, y_075 = data[:, 0], data[:, 1]
# CFD data from Fluent
x_075_fluent, y_075_fluent = load_xy_data('CFD for Nuclear Engineering/Lab_07-NLEVM/crosstream-velocity-075')
# take half of the data
# x_075_fluent = x_075_fluent[:len(x_075_fluent)//2]
# y_075_fluent = y_075_fluent[:len(y_075_fluent)//2]
# Normalize
x_075_fluent = (-np.array(x_075_fluent) + width)/width # Normalize to the half-width of the channel
y_075_fluent = np.array(y_075_fluent) / v_bulk # Normalize to the bulk velocity

# Wall shear stress normalized over density * bulk velocity ^2
# X data is z/half-width of the channel (-1 to 1)
data = np.genfromtxt('CFD for Nuclear Engineering/Lab_07-NLEVM/plot-data.csv', delimiter=',', skip_header=1)
x_tau, y_tau = data[:, 0], data[:, 1]
# CFD data from Fluent
x_tau_fluent, y_tau_fluent = load_xy_data('CFD for Nuclear Engineering/Lab_07-NLEVM/wall_shear')
x_tau_fluent = np.array(x_tau_fluent) - width /2
y_tau_fluent = np.array(y_tau_fluent) / (rho * v_bulk ** 2)  # Normalize to rho * U^2 



# Plot
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

ax[0].plot(x_05, y_05, label='x = -0.5')
ax[0].plot(x_05_fluent, y_05_fluent, label='x = Fluent -0.5')
ax[0].set_title('Normalized cross-stream velocity')
ax[0].set_xlabel('y')
ax[0].set_ylabel('u / U')
ax[0].legend()

ax[1].plot(x_05, y_05, label='x = -0.5')
ax[1].plot(x_075_fluent, y_075_fluent, label='x = Fluent -0.75')
ax[1].set_title('Normalized cross-stream velocity')
ax[1].set_xlabel('y')
ax[1].set_ylabel('u / U')
ax[1].legend()

ax[2].plot(x_tau, y_tau, label='Wall shear stress')
ax[2].plot(x_tau_fluent, y_tau_fluent, label='Fluent wall shear stress')
ax[2].set_title('Wall shear stress')
ax[2].set_xlabel('z')
ax[2].set_ylabel('tau / (rho * U^2)')
ax[2].legend()

plt.tight_layout()
plt.show()