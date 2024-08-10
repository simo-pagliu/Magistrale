import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 6
############################################################################################################
print("ALFRED")

############################################################################################################
# Define materials and compounds (7 fuel compositions + water)
############################################################################################################
materials = [
    {'name': "U-234", 'sigma_f': 0.8478, 'sigma_c': 0.1522, 'nu': 2.7, 'molar_mass': 234},
    {'name': "U-235", 'sigma_f': 1.2741, 'sigma_c': 0.1679, 'nu': 2.52, 'molar_mass': 235},
    {'name': "U-238", 'sigma_f': 0.1736, 'sigma_c': 0.1057, 'nu': 2.53, 'molar_mass': 238},
    {'name': "Pu-238", 'sigma_f': 1.6024, 'sigma_c': 0.2236, 'nu': 3.07, 'molar_mass': 238},
    {'name': "Pu-239", 'sigma_f': 1.7073, 'sigma_c': 0.1038, 'nu': 3.01, 'molar_mass': 239},
    {'name': "Pu-240", 'sigma_f': 0.9421, 'sigma_c': 0.1414, 'nu': 2.99, 'molar_mass': 240},
    {'name': "Pu-241", 'sigma_f': 1.6863, 'sigma_c': 0.1451, 'nu': 3.2, 'molar_mass': 241},
    {'name': "Pu-242", 'sigma_f': 0.7737, 'sigma_c': 0.1260, 'nu': 3.03, 'molar_mass': 242},
    {'name': "Am-241", 'sigma_f': 0.8505, 'sigma_c': 0.6207, 'nu': 3.5, 'molar_mass': 241},
    {'name': "O", 'sigma_f': 0.0000, 'sigma_c': 0.0564, 'nu': 0, 'molar_mass': 16},
    {'name': "Pb-204", 'sigma_f': 0.0000, 'sigma_c': 0.0138, 'nu': 0, 'molar_mass': 204},
    {'name': "Pb-206", 'sigma_f': 0.0000, 'sigma_c': 0.0011, 'nu': 0, 'molar_mass': 206},
    {'name': "Pb-207", 'sigma_f': 0.0000, 'sigma_c': 0.0015, 'nu': 0, 'molar_mass': 207},
    {'name': "Pb-208", 'sigma_f': 0.0000, 'sigma_c': 0.0002, 'nu': 0, 'molar_mass': 208},
]



compounds = [
    # MOX 1 Composition
    [
        {'name': "U-234", 'atom_fraction': 0.0002676767676767678},
        {'name': "U-235", 'atom_fraction': 0.05423131313131313},
        {'name': "U-238", 'atom_fraction': 26.71317777777778},
        {'name': "Pu-238", 'atom_fraction': 0.159948316498316},
        {'name': "Pu-239", 'atom_fraction': 3.884584343434344},
        {'name': "Pu-240", 'atom_fraction': 1.83624781144781},
        {'name': "Pu-241", 'atom_fraction': 0.413442476094276},
        {'name': "Pu-242", 'atom_fraction': 0.5189191919191919},
        {'name': "Am-241", 'atom_fraction': 0.08921296296296296},
        {'name': "O", 'atom_fraction': 66.3299663299663},
    ],
    
    # MOX 2 Composition
    [
        {'name': "U-234", 'atom_fraction': 0.0002484848484848484},
        {'name': "U-235", 'atom_fraction': 0.0503430303030303},
        {'name': "U-238", 'atom_fraction': 24.79789333333333},
        {'name': "Pu-238", 'atom_fraction': 0.204421750841751},
        {'name': "Pu-239", 'atom_fraction': 4.964688282828283},
        {'name': "Pu-240", 'atom_fraction': 2.346814276094276},
        {'name': "Pu-241", 'atom_fraction': 0.528401952861953},
        {'name': "Pu-242", 'atom_fraction': 0.6632040404040404},
        {'name': "Am-241", 'atom_fraction': 0.1140185185185185},
        {'name': "O", 'atom_fraction': 66.3299663299663},
    ],
    
    # Lead Composition --> Natuaral Isotopic Composition: https://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl?ele=Pb
    [
    {'name': "Pb-204", 'atom_fraction': 0.014},
    {'name': "Pb-206", 'atom_fraction': 0.241},
    {'name': "Pb-207", 'atom_fraction': 0.221},
    {'name': "Pb-208", 'atom_fraction': 0.524},
    ]

]

# Density of each compound
densities = [0.95 * 11.46, 0.95 * 11.46, 10.5] #MOX1, MOX2, Lead

# Volume occupied in the core by each compound
volumes = [0.262, 0.5217, 2.2] #MOX1, MOX2, Lead

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