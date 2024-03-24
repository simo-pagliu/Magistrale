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
    {'name': "Fe-56", 'sigma_f': 0, 'sigma_a': 0.0018, 'nu': 0, 'density': 7.87, 'molar_mass': 56, 'vol_fraction': 0.2, 'fuel': False},
    {'name': "Na-23", 'sigma_f': 0, 'sigma_a': 0.0087, 'nu': 0, 'density': 0.97, 'molar_mass': 23, 'vol_fraction': 0.5, 'fuel': False},
]

############################################################################################################
# Macroscopic cross section of the mixture and Nu*Sigma_fiss
############################################################################################################
Macro_abs = []
Macro_Fiss = []
Nu_Sigma_fiss = []

for ii in materials:
    Macro_abs.append(nf.macro(ii['sigma_a'], ii['density'], ii['molar_mass']))

    temp = nf.macro(ii['sigma_f'], ii['density'], ii['molar_mass'])
    Macro_Fiss.append(temp)

    Nu_Sigma_fiss.append(ii['nu'] * temp)

############################################################################################################
# Qualities (volume fractions)
############################################################################################################
quals = []
quals_fuel =[]
fuel_fraction = 0.3

for ii in materials:
    val = ii['vol_fraction']
    if ii['fuel']:
        quals.append(val*fuel_fraction)
        quals_fuel.append(val)
    else:
        quals.append(val)
        quals_fuel.append(0)

############################################################################################################
# Multiplication factor K_inf
############################################################################################################
eta = nf.mixture(Nu_Sigma_fiss, quals) / nf.mixture(Macro_abs, quals)     
f = nf.mixture(Macro_abs, quals_fuel) / nf.mixture(Macro_abs, quals)
p = 1
epsilon = 1

K_inf = eta * epsilon * p * f
str1 = f"The multiplication factor is {round(K_inf, 2)}"
print(str1)

############################################################################################################
# Weight fraction of the core
############################################################################################################
weight_fractions = nf.vol2w(quals, [ii['density'] for ii in materials])

fuel_tot = 0
for ii in materials: 
    if ii['fuel']:
        index = materials.index(ii)
        fuel_tot += weight_fractions[index]
str2 = f"The mass of the core is {round(fuel_tot, 4)*100} % fuel."
print(str2)

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_7.txt", "w") as f:
    f.write(f"{str1}\n")
    f.write(str2)