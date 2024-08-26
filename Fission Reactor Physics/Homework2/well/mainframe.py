import sympy as sp
import numpy as np
import nuclei_func as nf
import define_diffusion_equations as dde
import interface_boundary_conditions as ibc
import outer_boundary_conditions as obc

class Region:
        def __init__(self, Diff, Abs, Fiss, Nu, Temp, Pos1, Pos2, composition, power=0):
            self.Diffusion = Diff  # Diffusion coefficient
            self.Absorption = Abs  # Source term
            self.Fission = Fiss  # Sigma Fission
            self.Nu = Nu  # Number of Neutrons per Fission
            self.Temperature = Temp  # Temperature of the region
            self.Start = Pos1 # Starting Position of the region
            self.End = Pos2  # Ending Position of the region
            self.Composition = composition  # Composition of the region
            self.Power = power  # Power of the region

def simplify_system_with_zeros(equations):
    # Step 1: Identify zero constants
    zero_constants = {}
    for eq in equations:
        if eq.rhs == 0 and len(eq.lhs.free_symbols) == 1:
            # It's of the form Eq(Ci, 0)
            const = list(eq.lhs.free_symbols)[0]
            zero_constants[const] = 0

    # Step 2: Substitute zero constants in the system
    simplified_equations = []
    for eq in equations:
        if eq.lhs not in zero_constants and eq.rhs not in zero_constants:
            simplified_eq = eq.subs(zero_constants)
            simplified_equations.append(simplified_eq)
            print(f"Substituting {zero_constants} in {eq} gives {simplified_eq}")

    return simplified_equations, zero_constants

def main(regions):
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
    equations, fluxes = dde.define_diffusion_equations(regions, x, D, F, N, A, B)

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
        if region == last_region_right or region == last_region_left:
            print(f"The region {i+1} spanning from {region.Start} to {region.End} is a boundary region")
            boundary_cond = obc.outer_boundary_conditions(fluxes[i], x, D, F, N, A, B, region, regions)
            for ii in boundary_cond:
                boundaries.append(ii)

        # Apply interface boundary conditions
        if i < len(regions) and i > 0:  # Ensure we don't go out of bounds
            last_region = regions[i-1]
            if last_region.End == region.Start:
                print(f"The regions {i} and {i+1} are adjacent at {last_region.End}")
                interface_cond = ibc.interface_boundary_conditions(fluxes[i-1], fluxes[i], x, D, F, N, A, last_region, region)
                for ii in interface_cond:
                    interfaces.append(ii)
    
    ############################################################################################################
    # Power Condition
    ############################################################################################################
    powers = []
    #Find the region(s) with sigma_fission !=0
    fission_regions = [region for region in regions if region.Power != 0]
    # Now integrate the flux over the region
    for region in fission_regions:
        integrated_flux = sp.integrate(fluxes[1].rhs, (x, region.Start, region.End))
        power = sp.Eq(region.Fission * region.Nu * integrated_flux, region.Power)
        powers.append(power)

    ############################################################################################################
    # Save some outputs for the user
    ############################################################################################################
    # Save the fluxes, boundaries, interfaces and powers before substituting the values
    boundaries_eq = boundaries
    interfaces_eq = interfaces
    fluxes_eq = fluxes
    powers_eq = powers

    ############################################################################################################
    # Compute cross sections
    ############################################################################################################
    


    ############################################################################################################
    # Substitute all known values: region.Diffusion, region.Absorption, region.Fission, region.Nu, etc
    ############################################################################################################
    i_pwr = 0
    i_out = 0
    for i, region in enumerate(regions):
        # Identify the symbolg Bg{i+1} for the region
        B = sp.symbols(f'Bg_{i+1}', positive=True)
        # Subs it with (A - N*F)/D, using A,N,F and D from the region i
        B_val = sp.sqrt((region.Nu*region.Fission - region.Absorption)/region.Diffusion)

        # Subs values in all fluxes
        fluxes[i] = fluxes[i].subs({B: B_val, D: region.Diffusion, A: region.Absorption, F: region.Fission, N: region.Nu})

        # The buckling might appear anywhere in the equations, so we need to substitute it in all equations
        for j, pp in enumerate(powers):
            powers[j] = pp.subs(B,B_val)

        for j, bb in enumerate(boundaries):
            boundaries[j] = bb.subs(B,B_val)

        for j, jj in enumerate(interfaces):
            interfaces[j] = jj.subs(B,B_val)

        # Power condition only to regions with power
        if region.Fission != 0:
            # substitute the values for the power condition
            powers[i_pwr] = powers[i_pwr].subs({D: region.Diffusion, A: region.Absorption, F: region.Fission, N: region.Nu})
            i_pwr += 1

        # Boundary conditions only to boundary regions
        if region == last_region_right or region == last_region_left:
            # substitute the values for the boundary condition
            boundaries[i_out] = boundaries[i_out].subs({D: region.Diffusion, A: region.Absorption, F: region.Fission, N: region.Nu})
            i_out += 1
    
    ############################################################################################################
    # DEBUGGING
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
    # Simplify the system of equations
    ############################################################################################################
    print('\nSimplifying....')
    system = fluxes + boundaries + interfaces + powers
    system, zero_constants = simplify_system_with_zeros(system)

    # Display the results
    print("Zero Constants:")
    print(zero_constants)

    print("\nSimplified Equations:")
    for eq in system:
        print(eq)

    return equations, fluxes_eq, boundaries_eq, interfaces_eq, powers_eq, system