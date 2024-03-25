import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 1
############################################################################################################
# Consider a Boiling Water Reactor (BWR), operating at 1’000 psi. At this pressure, the density of water and steam are, respectively,  g/cm3 and  g/cm3. The microscopic cross sections of H and O at neutron speed  cm/s are  b and  b. Assume that  of the total volume is occupied by steam, compute the following and comment the results:
#     • Macroscopic total cross section of water 
#     • Macroscopic total cross section of steam 
#     • Macroscopic total cross section of the steam-water mixture 
#     • Macroscopic total cross section of water under atmospheric conditions and room temperature

pressure = 68.95 # bar
rho_water = 0.74 # g/cm3
rho_steam = 0.036 # g/cm3
sigma_H = 38 # b
sigma_O = 4.2 # b
quality = 0.4 # 40% of the volume is steam

############################################################################################################
# Macroscopic total cross sections
############################################################################################################

# Microscopic total cross section of water
sigma_water = (2*sigma_H + sigma_O)/3

# Macroscopic total cross section of water
Macro_sigma_water = nf.macro(sigma_H, rho_water, 18)

# Macroscopic total cross section of steam
Macro_sigma_steam = nf.macro(sigma_H, rho_steam, 18)

# Macroscopic total cross section of the steam-water mixture
quantities = [Macro_sigma_steam, Macro_sigma_water]
qualities = [quality, 1 - quality]

Macro_sigma_mixture = nf.mixture(quantities, qualities)

# Macroscopic total cross section of water under atmospheric conditions and room temperature
rho_water_atm = 1e-3 # g/cm3
Macro_sigma_water_atm = nf.macro(sigma_H, rho_water_atm, 18)

############################################################################################################
# Save the results to a file
############################################################################################################
str0 = "Solution to Exercise 1:\n"
str1 = f"Macroscopic total cross section of water: {Macro_sigma_water:.3f} 1/cm\n"
str2 = f"Macroscopic total cross section of steam: {Macro_sigma_steam:.3f} 1/cm\n"
str3 = f"Macroscopic total cross section of the steam-water mixture: {Macro_sigma_mixture:.3f} 1/cm\n"
str4 = f"Macroscopic total cross section of water under atmospheric conditions and room temperature:{Macro_sigma_water_atm:.2e} 1/cm\n"
text = str0 + str1 + str2 + str3 + str4
#write the text to a file
with open(".\Fission Reactor Physics\Homework1\Sol_1.txt", "w") as f:
    f.write(text)