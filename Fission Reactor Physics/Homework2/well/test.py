import sympy as sp
import mainframe as mf
from mainframe import Region
import nuclei_func as nf

############################################################################################################
# INPUT EXAMPLE
############################################################################################################

micro_abs_water = nf.mixture([1, 1],[2, 1]) # XSEC DATA ?
micro_abs_U235 = 1 # XSEC DATA ?
micro_fiss_U235 = 0.0001 # XSEC DATA ?

density_water = 1
density_U235 = density_water # NOT SURE

macro_abs_water = nf.macro(micro_abs_water, density_water, 18)
macro_abs_U235 = nf.macro(micro_abs_U235, density_U235, 235)
macro_fiss_U235 = nf.macro(micro_fiss_U235, density_U235, 235)

qual = sp.symbols('qual', positive=True, real=True, lower_than=1)

macro_fiss = nf.mixture([macro_fiss_U235, 0], [qual, 1-qual])
macro_abs = nf.mixture([macro_abs_water, macro_abs_U235], [1-qual, qual])

Reflector_SX = Region(1, 0.0007, 0, 0, 60, -sp.oo, 0, {'H': 2, 'O': 1})
Core = Region(1, 0.06, 0.05, 2.44, 60, 0, 50, {'H': 2, 'O': 1, 'U-235': qual}, 1e6)
Reflector_DX = Region(1, 0.0007, 0, 0, 60, 50, sp.oo, {'H': 2, 'O': 1})
regions = [Reflector_SX, Core, Reflector_DX]

############################################################################################################
# Solving the problem
############################################################################################################
equations, fluxes, boundaries, interfaces, powers, system = mf.main(regions)

############################################################################################################
# Results
############################################################################################################
# Print the equations
print('Diffusion equations:')
for eq in equations:
    print(eq)

# Print the fluxes
print('\nFluxes:')
for flux in fluxes:
    print(flux)

# Print the boundary conditions
print('\nBoundary conditions:')
for cond in boundaries:
    print(cond)

# Print the interface conditions
print('\nInterface conditions:')
for cond in interfaces:
    print(cond)

# Print the power conditions
print('\nPower conditions:')
for p in powers:
    print(p)

############################################################################################################
# Solving the system of equations
############################################################################################################
print('\nSolving....')
solution = sp.solve(system)
print(solution)