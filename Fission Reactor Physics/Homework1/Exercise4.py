import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 4
############################################################################################################
# Plot the macroscopic cross-section of uranium dioxide (UO2) as a function of the enrichment, 
# from natural composition to 100%. In the plot, clearly highlight the following regions:
#     • 0.72% to 20% (low-enriched uranium LEU)
#     • 20% to 85% (highly enriched uranium HEU)
#     •  85% (weapon-grade uranium WGU)

############################################################################################################
# Molar mass, varying with the enrichment
############################################################################################################
molar_mass_U235 = 235.0439299 # g/mol
molar_mass_U238 = 238.0507884 # g/mol
molar_mass_O16 = 15.99491461957 # g/mol

enrichment_vector = np.linspace(0.72,100,1000)/100 # ENRICHMENT is WEIGHT PERCENTAGE

# Calculate the molar fractions of the mixture, not normalized
molar_fractions = []
for enrichment in enrichment_vector:
    molar_fractions_temp =nf.w2mol([enrichment, 1-enrichment], [molar_mass_U235, molar_mass_U238]) # Convert enrichemnt to molar fraction
    molar_fractions_temp.append(2) # Add 2 Oxygen atoms
    molar_fractions.append(molar_fractions_temp)

molar_mass = [nf.mixture([molar_mass_U235, molar_mass_U238, molar_mass_O16], qualities, 'normalize') for qualities in molar_fractions]

############################################################################################################
# Microscopic cross section of the oxide, varying with the enrichment
############################################################################################################
micro_sigma_U238 = 11.1 # barn
micro_sigma_U235 = 680 # barn
micro_sigma_O16 = 4 # barn

cross_section = [nf.mixture([micro_sigma_U235, micro_sigma_U238, micro_sigma_O16], qualities, 'normalize') for qualities in molar_fractions]

############################################################################################################
# Density, varying with the enrichment
############################################################################################################
density_U235 = 19.1 # g/cm3
density_U238 = 19.1 # g/cm3
density_O16 = 5.24 # g/cm3

# Calculate the weight fraction of the mixture, not normalized
weight_fractions = []
for mol_frac in molar_fractions:
    weight_fractions_temp = nf.mol2w(mol_frac, [molar_mass_U235, molar_mass_U238, molar_mass_O16]) # Convert to weight fraction
    weight_fractions.append(weight_fractions_temp)

density = [nf.mixture([density_U235, density_U238, density_O16], qualities, 'normalize') for qualities in weight_fractions]


############################################################################################################
# Macroscopic cross section, varying with the enrichment
############################################################################################################
macro_sigma = [nf.macro(cross_section[ii], density[ii], molar_mass[ii]) for ii in range(len(enrichment_vector))]

############################################################################################################
# Plot as requested
############################################################################################################
plt.plot(enrichment_vector, macro_sigma, label='Macroscopic cross section', color='black', linewidth=2)
plt.plot(enrichment_vector, density/max(density)*max(macro_sigma), label='Density', linestyle='dotted', color='black')
plt.plot(enrichment_vector, molar_mass/max(molar_mass)*max(macro_sigma), label= 'Molar mass', linestyle='--', color='black')
plt.axvspan(0.72/100, 20/100, color='green', alpha=0.5, label='LEU')
plt.axvspan(20/100, 85/100, color='yellow', alpha=0.5, label='HEU')
plt.axvspan(85/100, 100/100, color='red', alpha=0.5, label='WGU')
plt.xlim(0.72/100,100/100)
plt.xlabel('Enrichment')
plt.ylabel('Macroscopic cross section [1/cm]')
plt.legend()
# save plot to a file
plt.savefig('.\Fission Reactor Physics\Homework1\Sol_4.png')
plt.show()



