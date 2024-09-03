import sympy as sp
import numpy as np
import copy
import nuclei_func as nf
import define_diffusion_equations as dde
import interface_boundary_conditions as ibc
import outer_boundary_conditions as obc


class Region:
        def __init__(self, Diff, Abs, Fiss, Nu, Pos1, Pos2, composition, power=0, sym=0):
            self.Diffusion = Diff  # Diffusion coefficient
            self.Absorption = Abs  # Source term
            self.Fission = Fiss  # Sigma Fission
            self.Nu = Nu  # Number of Neutrons per Fission
            self.Start = Pos1 # Starting Position of the region
            self.End = Pos2  # Ending Position of the region
            self.Composition = composition  # Composition of the region
            self.Power = power  # Power of the region
            self.Symmetry = sym # To which region is this symmetric to (0 if not symmetric)

def compute(simplified_equations, regions):
    import re
    ############################################################################################################
    # Substitute all known values: region.Diffusion, region.Absorption, region.Fission, region.Nu, etc
    ############################################################################################################

    # Identify zero constants
    integration_constant_pattern = re.compile(r'C_\d+')
    zero_constants = []
    for eq in simplified_equations:
        if eq.rhs == 0 and 'x' not in str(eq.lhs) and sp.count_ops(eq.lhs) <= 1:
            # Check if the LHS contains any integration constants
            temp = integration_constant_pattern.findall(str(eq.lhs))
            print(f"Zero constant found in {eq} is {temp}")
            for t in temp:
                zero_constants.append(t)

    # Identify the region-specific symbols for the current region
    for i, region in enumerate(regions):
        D_i = sp.symbols(f'D_{i+1}', positive=True)
        F_i = sp.symbols(f'F_{i+1}', positive=True)
        A_i = sp.symbols(f'A_{i+1}', positive=True)
        N_i = sp.symbols(f'N_{i+1}', positive=True)
        B_i = sp.symbols(f'Bg_{i+1}', positive=True)
        L_i = sp.symbols(f'L_{i+1}', positive=True)
        x_i = sp.symbols(f'x_{i+1}', real=True) # The interface is at the end of the left region

        # Calculate the value of B_i for the region
        # B_val = 0.05624 #sp.sqrt((region.Nu * region.Fission - region.Absorption) / region.Diffusion)
        # print(f"Region {i+1} has B = {B_val}")
        # L_val = sp.sqrt((region.Diffusion / region.Absorption))
        x_i_val = region.End

        # Define the substitution dictionary
        substitution_dict = {
            #L_i: L_val,
            #B_i: B_val,
            D_i: region.Diffusion,
            A_i: region.Absorption,
            F_i: region.Fission,
            N_i: region.Nu,
            x_i: x_i_val
        }

        # Integration constants
        if region.Composition == 'h':
            C_1 = sp.symbols(f'C_{i*2+1}', function=True)
            C_2 = sp.symbols(f'C_{i*2+2}', function=True)
        else:
            C_1 = sp.symbols(f'C_{i*2+1}', real=True)
            C_2 = sp.symbols(f'C_{i*2+2}', real=True)

        if f'C_{i*2+1}' in zero_constants:
            # Add a substitution to the dictionary
            substitution_dict[C_1] = 0
        
        if f'C_{i*2+2}' in zero_constants:
            # Add a substitution to the dictionary
            substitution_dict[C_2] = 0

        print(f"Substitution dictionary for region {i+1}: {substitution_dict}")
        
        # Apply the substitutions
        for j, eq in enumerate(simplified_equations):
            simplified_equations[j] = eq.subs(substitution_dict)
    
    # Check if any symbols were not substituted
    for eq in simplified_equations:
        for symbol in substitution_dict.keys():
            if symbol in eq.free_symbols:
                print(f"Warning: Symbol {symbol} was not substituted in equation {eq}")

    return simplified_equations

def main(regions, Symmetric=False):
    ############################################################################################################
    # Define symbols
    ############################################################################################################
    x = sp.symbols('x')
    D = sp.symbols('D', positive=True)  # Diffusion coefficient
    F = sp.symbols('F', positive=True)  # Fission Cross Section
    N = sp.symbols('N', positive=True)  # Number of Neutrons per Fission
    A = sp.symbols('A', positive=True, real=True, greater_than=F)  # Absorption Cross Section
    B = sp.symbols('B', positive=True)  # Buckling
    

    ############################################################################################################
    # Define the diffusion equations for each region
    ############################################################################################################
    equations, fluxes = dde.define_diffusion_equations(regions, x)

    ############################################################################################################
    # Apply boundary conditions, region by region
    ############################################################################################################
    boundaries = []
    interfaces = []

    # Get the region with the greatest positive position
    last_region_right = max(regions, key=lambda region: region.Start)
    # Get the region with the smallest negative position
    last_region_left = min(regions, key=lambda region: region.Start)

    for i, region in enumerate(regions):
        # Apply boundary conditions at the boundaries of the reactor
        # If the problem is symmetric, the symmetry condition is added by the outer_boundary_conditions function
        if region == last_region_right or region == last_region_left:
            print(f"The region {i+1} spanning from {region.Start} to {region.End} is a boundary region")
            boundary_cond = obc.outer_boundary_conditions(fluxes[i], x, region, regions, Symmetric)
            for ii in boundary_cond:
                boundaries.append(ii)
    
        # Apply interface boundary conditions
        if i < len(regions) and i > 0:  # Ensure we don't go out of bounds
            last_region = regions[i-1]
            if last_region.End == region.Start:
                print(f"The regions {i} and {i+1} are adjacent at {last_region.End}")
                interface_cond = ibc.interface_boundary_conditions(fluxes[i-1], fluxes[i], x, last_region, region, regions)
                for ii in interface_cond:
                    interfaces.append(ii)
    
    ############################################################################################################
    # Power Condition
    ############################################################################################################
    powers = []
    #Find the region(s) with sigma_fission !=0
    fission_regions = [region for region in regions if region.Power != 0]
    # Average energy released per fission
    energy_per_fission = 211.5 * 1.602177e-13 # MeV to Joules

    for region in fission_regions:
        index = regions.index(region)
        integrated_flux = sp.integrate(fluxes[index].rhs, (x, region.Start, region.End))
        power = sp.Eq(region.Fission * energy_per_fission * integrated_flux, region.Power)
        powers.append(power)

    ############################################################################################################
    # DEBUGGING
    ############################################################################################################
    # Print the equations
    print('Diffusion equations:')
    for eq in equations:
        print(eq)

    # Print the fluxes
    print('\nFluxes:')
    for eq in fluxes:
        print(eq)

    # Print the boundary conditions
    print('\nBoundary conditions:')
    for eq in boundaries:
        print(eq)

    # Print the interface conditions
    print('\nInterface conditions:')
    for eq in interfaces:
        print(eq)

    # Print the power conditions
    print('\nPower conditions:')
    for eq in powers:
        print(eq)

    return equations, fluxes, boundaries, interfaces, powers