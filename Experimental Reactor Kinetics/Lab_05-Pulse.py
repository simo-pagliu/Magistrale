#############################################################################
# Data from the pulse experiment
# rod position[digits], reacitivity insertion[$], max power[MW], energy[MWs], temperature [°C], FWHM [ms]
data = {
    "rod position": [
        588,
        565,
        541,
        517,
        492,
        467
    ],
    "reactivity insertion": [
        1.0,
        1.2,
        1.4,
        1.6,
        1.8,
        2.0
    ],
    "max power": [
        0.0,
        0.6,
        3.8,
        23.2,
        64.3,
        130.0
    ],
    "energy": [
        0.0,
        0.0,
        0.4,
        1.9,
        3.9,
        5.8
    ],
    "temperature": [
        0.0,
        30.0,
        165.0,
        206.0,
        238.0,
        267.0
    ],
    "FWHM": [
        0.0,
        800,
        2063,
        104,
        58,
        40
    ]
}
#############################################################################
import matplotlib.pyplot as plt
import numpy as np

# Initialize the figure and subplots
fig, axs = plt.subplots(1, 4, figsize=(16, 4))

# Pulse points
pulse_points = [1, 2, 3, 4, 5, 6]

# How many pulses from the first one should we not consider
n = 3

#############################################################################
# MAX POWER
rho_2 = np.array(data["reactivity insertion"])**2
p_max = data["max power"]

# Linear interpolation of the data
m, b = np.polyfit(rho_2[n:], p_max[n:], 1)

# Plot the data
axs[0].plot(rho_2, p_max, "o", label="Data")
axs[0].plot(rho_2, m * rho_2 + b, '--', label="Linear fit")
axs[0].legend()
axs[0].set_title(r"Max Power")
axs[0].set_ylabel(r"$Power [MW]$")
axs[0].set_xlabel(r"$\rho^2 [\$]$")
axs[0].grid()

# Secondary x-axis for pulse points
secax = axs[0].secondary_xaxis("top")
secax.set_xticks(rho_2)
secax.set_xticklabels(pulse_points)
secax.set_xlabel("Pulse")
#############################################################################

#############################################################################
# ENERGY
energy = data["energy"]
rho_prime = np.array(data["reactivity insertion"]) - 1

# Linear interpolation of the data
m, b = np.polyfit(rho_prime[n:], energy[n:], 1)

# Plot the data
axs[1].plot(rho_prime, energy, "o", label="Data")
axs[1].plot(rho_prime, m * rho_prime + b, '--', label="Linear fit")
axs[1].legend()
axs[1].set_title(r"Energy")
axs[1].set_ylabel(r"$Energy [MWs]$")
axs[1].set_xlabel(r"$\rho' [\$]$")
axs[1].grid()

# Secondary x-axis for pulse points
secax = axs[1].secondary_xaxis("top")
secax.set_xticks(rho_prime)
secax.set_xticklabels(pulse_points)
secax.set_xlabel("Pulse")
#############################################################################

#############################################################################
# TEMPERATURE
temp = data["temperature"]

# Linear interpolation of the data
m, b = np.polyfit(energy[n:], temp[n:], 1)

# Plot the data
axs[2].plot(energy, temp, "o", label="Data")
axs[2].plot(energy, m * np.array(energy) + b, '--', label="Linear fit")
axs[2].legend()
axs[2].set_title(r"Temperature")
axs[2].set_ylabel(r"$Temperature [°C]$")
axs[2].set_xlabel(r"$Energy [MWs]$")
axs[2].grid()

# Secondary x-axis for pulse points
secax = axs[2].secondary_xaxis("top")
secax.set_xticks(energy)
secax.set_xticklabels(pulse_points)
secax.set_xlabel("Pulse")
#############################################################################

#############################################################################
# FWHM
fwhm = data["FWHM"]
one_over_rho = np.array([1 / r for r in data["reactivity insertion"]])

# Linear interpolation of the data
m, b = np.polyfit(one_over_rho[n:], fwhm[n:], 1)

# Plot the data
axs[3].plot(one_over_rho, fwhm, "o", label="Data")
axs[3].plot(one_over_rho, m * one_over_rho + b, '--', label="Linear fit")
axs[3].legend()
axs[3].set_title(r"FWHM")
axs[3].set_ylabel(r"$FWHM [ms]$")
axs[3].set_xlabel(r"$1/\rho [\$]$")
axs[3].grid()

# Secondary x-axis for pulse points
secax = axs[3].secondary_xaxis("top")
secax.set_xticks(one_over_rho)
secax.set_xticklabels(pulse_points)
secax.set_xlabel("Pulse")
#############################################################################

# Show the plots
plt.tight_layout()
plt.show()