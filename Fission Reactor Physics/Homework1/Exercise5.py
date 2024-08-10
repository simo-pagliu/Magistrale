import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 5
############################################################################################################
# Equal volumes of graphite and iron are mixed. 15% of the volume of the resulting mixture is occupied by air pockets. 
# Find the total macroscopic cross section given the following data:
#   • Graphite: 4.8 barn, density 1.6 g/cm3
#   • Iron: 13.6 barn, density 7.7 g/cm3
# Assess whether it is reasonable to neglect the cross section of air. 
# Plot the value of the cross-section of air as a function of the occupied volume fraction.

# Data
micro_sigma_graphite = 4.8 # barn
density_graphite = 1.6 # g/cm3
micro_sigma_iron = 13.6 # barn
density_iron = 7.7 # g/cm3

volume_fraction = np.linspace(0,1,1000) # Volume fraction of the mixture

############################################################################################################
# Cross Section of air as a mixture of oxygen and nitrogen
############################################################################################################
micro_sigma_oxygen = 4 # barn
micro_sigma_nitrogen = 0.2 # barn
sigma_air = nf.mixture([micro_sigma_oxygen, micro_sigma_nitrogen], [0.21, 0.79], 'normalize')
density_air = 1.225e-3 # g/cm3

############################################################################################################
# Cross Section of air as a mixture of oxygen and nitrogen
############################################################################################################
rhos = [density_graphite, density_iron, density_air] # g/cm3
MMs = [12, 56, 28.97] # g/mol
molar_fraction = [] # initialize the molar fraction list
mass_fraction = [] # initialize the mass fraction list
for f in volume_fraction:
    w_temp = nf.vol2w([0.5-f/2, 0.5-f/2, f], rhos) # first calculate the weight fraction
    mass_fraction.append(w_temp)
    m_temp = nf.w2mol(w_temp, MMs) # then calculate the molar fraction
    molar_fraction.append(m_temp) 

############################################################################################################
# Cross Section of the mixture
############################################################################################################
macro_sigma_graphite = nf.macro(micro_sigma_graphite, density_graphite, 12)
macro_sigma_iron = nf.macro(micro_sigma_iron, density_iron, 56)
macro_sigma_air = nf.macro(sigma_air, density_air, 28.97)
macro_sigma = [nf.mixture([macro_sigma_graphite, macro_sigma_iron, macro_sigma_air], ii, 'normalize') for ii in mass_fraction]

############################################################################################################
# Can we neglect the air cross section when it's 15% of the volume?
############################################################################################################
index_15 = np.abs(volume_fraction - 0.15).argmin() # find the index closest to 15%  

macro_sigma_15 = macro_sigma[index_15]
str_1 = f"The macroscopic cross section at 15% air is {macro_sigma_15} 1/cm."
print(str_1)

comparison = 1 - macro_sigma_15/macro_sigma[0]
if comparison > 0.01: # 1% threshold
    str_2 = f"It is NOT reasonable to neglect the cross section of air, since it changes the cross-section by {round(comparison,6)*100} %."
else:
    str_2 = f"It is reasonable to neglect the cross section of air, since it changes the cross-section by {round(comparison,6)*100} %."
print(str)

############################################################################################################
# Save solution to a file
############################################################################################################
str = str_1 + "\n" + str_2
with open(".\Fission Reactor Physics\Homework1\Sol_5.txt", "w") as f:
    f.write(str)

############################################################################################################
# Plot as requested and save image
############################################################################################################
plt.figure()
plt.plot(volume_fraction, macro_sigma, label='Macroscopic cross section', color='black', linewidth=2)
plt.axvline(0.15, color='red', linestyle='--', label="0.15 air")
plt.xlim(0,1)
plt.xlabel('Volume fraction [/100]')
plt.xticks(np.arange(0,1.05,0.05))
plt.ylabel('Macroscopic cross section [1/cm]')
plt.legend()
plt.grid()
plt.savefig('.\Fission Reactor Physics\Homework1\Sol_5.png') # save plot to a file
plt.show()