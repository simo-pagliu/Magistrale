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
air_volume_fraction = 21 # 21% oxygen and 79% nitrogen
sigma_air = nf.mixture([micro_sigma_oxygen, micro_sigma_nitrogen], [0.21, 0.79], 'normalize')
density_air = 1.225e-3 # g/cm3

############################################################################################################
# Cross Section of air as a mixture of oxygen and nitrogen
############################################################################################################
rhos = [density_graphite, density_iron, density_air] # g/cm3
MMs = [12, 56, 28.97] # g/mol
molar_fraction = [] # initialize the molar fraction list
for f in volume_fraction:
    w_temp = nf.vol2w([0.5-f/2, 0.5-f/2, f], rhos) # first calculate the weight fraction
    m_temp = nf.w2mol(w_temp, MMs) # then calculate the molar fraction
    molar_fraction.append(m_temp) 

############################################################################################################
# Cross Section of the mixture
############################################################################################################
sigmas = [micro_sigma_graphite, micro_sigma_iron, sigma_air]
sigma_mix = [nf.mixture(sigmas, mol, 'normalize') for mol in molar_fraction]
MM_mix = [nf.mixture(MMs, mol, 'normalize') for mol in molar_fraction]
density_mix = [nf.mixture(rhos, [0.5-vol/2, 0.5-vol/2, vol], 'normalize') for vol in volume_fraction]
macro_sigma = [nf.macro(sigma_mix[ii], density_mix[ii], MM_mix[ii]) for ii in range(len(sigma_mix))]

############################################################################################################
# Can we neglect the air cross section when it's 15% of the volume?
############################################################################################################

# find the index closest to 15%  
index_15 = np.abs(volume_fraction - 0.15).argmin()
comparison = 1 - macro_sigma[index_15]/macro_sigma[0]

if comparison > 0.01: # 1% threshold
    str = f"It is NOT reasonable to neglect the cross section of air, since it changes the cross-section by {round(comparison,2)*100} %."
else:
    str = f"It is reasonable to neglect the cross section of air, since it changes the cross-section by {round(comparison,2)*100} %."
print(str)

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_5.txt", "w") as f:
    f.write(str)

############################################################################################################
# Plot as requested and save image
############################################################################################################
plt.figure()
macro_sigma_var = [nf.macro(sigma_air, density_mix[ii], MM_mix[ii]) for ii in range(len(density_mix))]
plt.plot(volume_fraction, macro_sigma, label='Macroscopic cross section', color='black', linewidth=2)
plt.plot(volume_fraction, macro_sigma_var, label='Macroscopic cross section of air only', color='red', linewidth=2)
plt.plot(volume_fraction, density_mix/max(density_mix)*max(macro_sigma), label='Density', linestyle='dotted', color='black')
plt.plot(volume_fraction, MM_mix/max(MM_mix)*max(macro_sigma), label= 'Molar mass', linestyle='--', color='black')
plt.axvline(0.15, color='red', linestyle='--', label="0.15 air")
plt.xlim(0,1)
plt.xlabel('Volume fraction [/100]')
plt.xticks(np.arange(0,1.05,0.05))
plt.ylabel('Macroscopic cross section [1/cm]')
plt.legend()
plt.grid()
plt.savefig('.\Fission Reactor Physics\Homework1\Sol_5.png') # save plot to a file
plt.show()