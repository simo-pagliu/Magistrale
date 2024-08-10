import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 6
############################################################################################################
print("NuScale")

############################################################################################################
# Data
############################################################################################################
materials = [
    {'name': "U-235", 'sigma_f': 577, 'sigma_c': 101, 'nu': 2.43, 'molar_mass': 235},
    {'name': "U-238", 'sigma_f': 0, 'sigma_c': 2.73, 'nu': 0,  'molar_mass': 238},
    {'name': "O", 'sigma_f': 0, 'sigma_c': 4.2, 'nu': 0, 'molar_mass': 16},
    {'name': "H", 'sigma_f': 0, 'sigma_c': 0.33, 'nu': 0, 'molar_mass': 1},
    {'name': "Gd", 'sigma_f': 0, 'sigma_c': 46000, 'nu': 0, 'molar_mass': 157},
]

compounds = [
    # Fuel 1
    [
        {'name': "U-235", 'atom_fraction': 0.00506299656514596},
        {'name': "U-238", 'atom_fraction': 0.328270393583015},
        {'name': "O", 'atom_fraction': 0.666666609851839},
    ],
    
    # Fuel 2
    [
        {'name': "U-235", 'atom_fraction': 0.00540046072633078},
        {'name': "U-238", 'atom_fraction': 0.327931632163372},
        {'name': "O", 'atom_fraction': 0.666667907110297},
    ],
    
    # Fuel 3
    [
        {'name': "U-235", 'atom_fraction': 0.008437244494789843},
        {'name': "U-238", 'atom_fraction': 0.324895936869628},
        {'name': "O", 'atom_fraction': 0.666666681815581},
    ],
    
    # Fuel 4
    [
        {'name': "U-235", 'atom_fraction': 0.00877462047195195},
        {'name': "U-238", 'atom_fraction': 0.324558674989504},
        {'name': "O", 'atom_fraction': 0.666666670453854},
    ],
    
    # Fuel 5
    [
        {'name': "U-235", 'atom_fraction': 0.0136653089909534},
        {'name': "U-238", 'atom_fraction': 0.319667143922179},
        {'name': "O", 'atom_fraction': 0.666667225186868},
    ],
    
    # Fuel 6
    [
        {'name': "U-235", 'atom_fraction': 0.0153792077677215},
        {'name': "U-238", 'atom_fraction': 0.318345227518712},
        {'name': "O", 'atom_fraction': 0.666275564713567},
    ],
    
    # Fuel 7
    [
        {'name': "U-235", 'atom_fraction': 0.0138566447991035},
        {'name': "U-238", 'atom_fraction': 0.28701296607538},
        {'name': "O", 'atom_fraction': 0.660174216147815},
        {'name': "Gd", 'atom_fraction': 0.038956172707702},
    ],
    
    # Water
    [
        {'name': "O", 'atom_fraction': 0.333333333333333},
        {'name': "H", 'atom_fraction': 0.666666666666666},
    ]
]

# Density of each compound
densities = [0.96 * 10.53] * 7 # Fuels have the same density
densities.append(0.7355) # At last we add the water density

# Volume occupied in the core by each compound
volumes = [0.09646, 0.04861, 0.09716, 0.05951, 0.0962, 0.04507, 0.003171, 0.882]

############################################################################################################
# Compute the six factors
############################################################################################################
eta, f = nf.six_factors(compounds, densities, materials, volumes)
print(f"eta: {eta}")
print(f"f: {f}")
print(f"K_inf: {eta*f}")

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_6.txt", "w") as f:
    f.write("\n")