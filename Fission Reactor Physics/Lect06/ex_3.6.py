from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np


# Add the parent directory to the sys.path list to import END_requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ENDF_requests as ENDF

## THIS PART HERE IS NEEDED ONLY ONCE TO CHOOSE THE IDs of the datasets

#MT codes at https://www-nds.iaea.org/exfor/helpe/help_reaction.htm

#datasets for U-235 fission 24020202
# ENDF.database_info("U-235", 18, "SIG")

#datasets for U-235 absorption 24014142
# ENDF.database_info("U-235", 102, "SIG")

#datasets for U-238 absorption 24020696
#ENDF.database_info("U-238", 102, "SIG")

Energy_Eval = 25e-3 #eV energy at which we evaluate cross sections

E_values, Sig_values = ENDF.data_get(24020202)
f_235 = interpolate.interp1d(E_values, Sig_values, kind='linear')
f_235 = f_235(Energy_Eval)
print("Fission of 235: ", f_235)

E_values, Sig_values = ENDF.data_get(24014142)
g_235 = interpolate.interp1d(E_values, Sig_values, kind='linear')
a_235 = g_235(Energy_Eval) + f_235
print("Absorbtion of 235 (gamma+fission): ", a_235)

f_238 = 0 #obviuosly its 0, i just wanted to write the formula in the most general way

E_values, Sig_values = ENDF.data_get(24020696)
g_238 = interpolate.interp1d(E_values, Sig_values, kind='linear')
a_238 = g_238(Energy_Eval) + f_238
print("Absorbtion of 238 (gamma+fission=0): ", a_238)

enrichment = np.linspace(0, 1, 100)
nu = 2.432 + 0.066*Energy_Eval #average number of neutrons per fission
print("Nu: ", nu)

print("Disclaimer: we are NOT taking into account the moderator or any other material that could absorb neutrons. This is a very simplified model.")
eta = (enrichment*nu*f_235 + (1-enrichment)*f_238) / (enrichment*a_235 + (1-enrichment)*a_238)

# Plot Eta vs Enrichment
plt.plot(enrichment, eta)
plt.xlabel('Enrichment [0 ~ 1]')
plt.ylabel('Eta [#(n) produced per (n) absorbed in fuel]')
plt.grid()
plt.show()
