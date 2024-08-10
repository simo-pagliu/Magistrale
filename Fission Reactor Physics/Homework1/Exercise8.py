import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 8
############################################################################################################
# Suppose the non-leakage probability for a sodium cooled fast reactor specified in assignment 7 is 0.90. 
# Using the data from assignment 7, adjust the volume fractions of PuO2 and UO2 in the fuel so that κ = 1. 
# What is the percentage in the fuel by volume?

############################################################################################################
# Loop over an array of Pu volume fractions
############################################################################################################
# Initialize the K values array
K_vals = []

# Define the range of Pu volume fractions
min = 0
# Limit at a reasonable value given the result of Ex.7 : 
# K_inf=1.33 with volume fraction = 0.15, with P_NL=0.9 --> K_real = 1.197
# We are required to get K_real = 1
# Therefore it's reasonable to expected a volume fraction lower then 0.15
max = 0.15
steps = 10000
pu_frac = np.linspace(min,max,steps)

# Loop over the Pu volume fractions
for jj in pu_frac:
    materials = [
        {'name': "Pu-239", 'sigma_f': 1.95, 'sigma_a': 2.4, 'nu': 2.98, 'density': 11, 'molar_mass': 239+32, 'vol_fraction': jj, 'fuel': True},
        {'name': "U-238", 'sigma_f': 0.05, 'sigma_a': 0.404, 'nu': 2.47, 'density': 11, 'molar_mass': 238+32, 'vol_fraction': 1-jj, 'fuel': True},
        {'name': "Fe-56", 'sigma_f': 0, 'sigma_a': 0.0087, 'nu': 0, 'density': 7.87, 'molar_mass': 56, 'vol_fraction': 0.2, 'fuel': False},
        {'name': "Na-23", 'sigma_f': 0, 'sigma_a': 0.0018, 'nu': 0, 'density': 0.97, 'molar_mass': 23, 'vol_fraction': 0.5, 'fuel': False},
    ]
    K_inf, PuO2_mass_percent, UO2_mass_percent = nf.compute_k(materials)
    K_real = K_inf * 0.9
    K_vals.append(K_real)

############################################################################################################
# Find the closest to 1 and print the corresponding Pu volume fraction
############################################################################################################
index = np.argmin(abs(np.array(K_vals)-1))
str = f"The Pu volume fraction corresponding to the K value closest to 1 is: {pu_frac[index]:.4f}"
print(str)

############################################################################################################
# Plot the K values vs Pu fraction (not required)
############################################################################################################
plt.plot(pu_frac,K_vals)
plt.xlabel("Pu fraction")
plt.ylabel("K")
plt.title("K values vs Pu fraction")
plt.grid()
plt.show()

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_8.txt", "w") as f:
    f.write(str)