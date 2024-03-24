import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 8
############################################################################################################
# Suppose the non-leakage probability for a sodium cooled fast reactor specified in assignment 7 is 0.90. 
# Using the data from assignment 7, adjust the volume fractions of PuO2 and UO2 in the fuel so that κ = 1. 
# What is the percentage in the fuel by volume?
materials = [
    {'name': "Pu-239", 'sigma_f': 1.95, 'sigma_a': 2.4, 'nu': 2.98, 'density': 11, 'molar_mass': 239+32},
    {'name': "U-238", 'sigma_f': 0.05, 'sigma_a': 0.404, 'nu': 2.47, 'density': 11, 'molar_mass': 238+32},
    {'name': "Fe-56", 'sigma_f': 0, 'sigma_a': 0.0018, 'nu': 0, 'density': 7.87, 'molar_mass': 56},
    {'name': "Na-23", 'sigma_f': 0, 'sigma_a': 0.0087, 'nu': 0, 'density': 0.97, 'molar_mass': 23},
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
# Compute an array of K values
############################################################################################################
K_vals = []
fuel_fraction = 0.3

#here I set the range of values to loop over
min = 0
max = 0.1
steps = 10000
pu_frac = np.linspace(min,max,steps)

#loop over the range of values
for jj in pu_frac:

    #compute fractions
    quals_fuel = [jj, 1-jj, 0, 0]
    quals = [jj*fuel_fraction, (1-jj)*fuel_fraction, 0.2, 0.5]

    #calculate the multiplication factor
    eta = nf.mixture(Nu_Sigma_fiss, quals, 'normalize') / nf.mixture(Macro_abs, quals, 'normalize')     
    f = nf.mixture(Macro_abs, quals_fuel, 'normalize') / nf.mixture(Macro_abs, quals, 'normalize')
    p = 0.9 #non-leakage probability - difference from assignment 7
    epsilon = 1

    #add value to array
    K_vals.append(eta * epsilon * p * f)

#find the index of the K value closest to 1
index = np.argmin(abs(np.array(K_vals)-1))
print(K_vals[index]) # print the K value closest to 1
print(pu_frac[index]) # print the Pu fraction corresponding to the K value closest to 1

#plot k values
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
    f.write("\n")