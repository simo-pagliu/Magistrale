import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 7
############################################################################################################
# Consider a sodium-cooled fast reactor, fuelled with PuO2 mixed with depleted UO2. 
# The structural material is iron. Averaged over the spectrum of fast neutrons, 
# the microscopic cross-sections and densities are the following:
#
# PuO2 sigma_f=1.95 sigma_a=2.4 nu=2.98 density=11 g/cm3 molar_mass=239+32 g/mol
# UO2 sigma_f=0.05 sigma_a=0.404 nu=2.47 density=11 g/cm3 molar_mass=238+32 g/mol
# Na sigma_f=0 sigma_a=0.0018 nu=0 density=0.97 g/cm3 molar_mass=23 g/mol
# Fe sigma_f=0 sigma_a=0.0087 nu=0 density=7.87 g/cm3 molar_mass=56 g/mol
#
# The fuel is 15% PuO2 and 85% UO2 by volume. 
# The volumetric composition of the core is 30% fuel, 50% coolant and 20% structural material. 
# Calculate if the values of  for plutonium and uranium in the fast spectrum are 2.98 and 2.47, respectively, 
# and that the cross sections of oxygen can be neglected. 
# What fraction of the mass of the core does the fuel account for?
materials = [
    {'name': "Pu-239", 'sigma_f': 1.95, 'sigma_a': 2.4, 'nu': 2.98, 'density': 11, 'molar_mass': 239+32, 'vol_fraction': 0.15, 'fuel': True},
    {'name': "U-238", 'sigma_f': 0.05, 'sigma_a': 0.404, 'nu': 2.47, 'density': 11, 'molar_mass': 238+32, 'vol_fraction': 0.85, 'fuel': True},
    {'name': "Fe-56", 'sigma_f': 0, 'sigma_a': 0.0087, 'nu': 0, 'density': 7.87, 'molar_mass': 56, 'vol_fraction': 0.2, 'fuel': False},
    {'name': "Na-23", 'sigma_f': 0, 'sigma_a': 0.0018, 'nu': 0, 'density': 0.97, 'molar_mass': 23, 'vol_fraction': 0.5, 'fuel': False},
]

# Call the function in nuclei_func since it is in common with exercise 8 and I didn't want to copy paste it in two scripts
K_inf, PuO2_mass_percent, UO2_mass_percent = nf.compute_k(materials)

############################################################################################################
# Print the results
############################################################################################################
str1 = f"The multiplication factor is {round(K_inf, 2)}"
print(str1)
str2 = f"The mass of the core is {PuO2_mass_percent}% PuO2 and {UO2_mass_percent}% UO2."
print(str2)

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_7.txt", "w") as f:
    f.write(f"{str1}\n")
    f.write(str2)