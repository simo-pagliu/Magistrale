import sympy as sp
import numpy as np
import copy
import nuclei_func as nf
import define_diffusion_equations as dde
import interface_boundary_conditions as ibc
import outer_boundary_conditions as obc


class Region:
        def __init__(self, Diff, Abs, Fiss, Nu, Temp, Pos1, Pos2, composition, power=0, sym=0):
            self.Diffusion = Diff  # Diffusion coefficient
            self.Absorption = Abs  # Source term
            self.Fission = Fiss  # Sigma Fission
            self.Nu = Nu  # Number of Neutrons per Fission
            self.Temperature = Temp  # Temperature of the region
            self.Start = Pos1 # Starting Position of the region
            self.End = Pos2  # Ending Position of the region
            self.Composition = composition  # Composition of the region
            self.Power = power  # Power of the region
            self.Symmetry = sym # To which region is this symmetric to (0 if not symmetric)

def compute(fluxes, boundaries, interfaces, powers, regions):
    ############################################################################################################
    # Substitute all known values: region.Diffusion, region.Absorption, region.Fission, region.Nu, etc
    ############################################################################################################
    for i, region in enumerate(regions):
        # Identify the region-specific symbols for the current region
        D_i = sp.symbols(f'D_{i+1}', positive=True)
        F_i = sp.symbols(f'F_{i+1}', positive=True)
        A_i = sp.symbols(f'A_{i+1}', positive=True)
        N_i = sp.symbols(f'N_{i+1}', positive=True)
        B_i = sp.symbols(f'Bg_{i+1}', positive=True)
        L_i = sp.symbols(f'L_{i+1}', positive=True)
        x_i = sp.symbols(f'x_{i+1}', positive=True) # The interface is at the end of the left region
        
        # Calculate the value of B_i for the region
        B_val = sp.sqrt((region.Nu * region.Fission - region.Absorption) / region.Diffusion)
        print(f"Region {i+1} has B = {B_val}")
        L_val = sp.sqrt((region.Diffusion / region.Absorption))
        x_i_val = region.End

        # Substitute values in all fluxes for the current region
        fluxes[i] = fluxes[i].subs({
            L_i: L_val,
            B_i: B_val,
            D_i: region.Diffusion,
            A_i: region.Absorption,
            F_i: region.Fission,
            N_i: region.Nu,
            x_i: x_i_val
        })

        for j, pp in enumerate(powers):
            powers[j] = pp.subs({
            L_i: L_val,
            B_i: B_val,
            D_i: region.Diffusion,
            A_i: region.Absorption,
            F_i: region.Fission,
            N_i: region.Nu,
            x_i: x_i_val
        })

        for j, bb in enumerate(boundaries):
            boundaries[j] = bb.subs({
            L_i: L_val,
            B_i: B_val,
            D_i: region.Diffusion,
            A_i: region.Absorption,
            F_i: region.Fission,
            N_i: region.Nu,
            x_i: x_i_val
        })

        for j, jj in enumerate(interfaces):
            interfaces[j] = jj.subs({
            L_i: L_val,
            B_i: B_val,
            D_i: region.Diffusion,
            A_i: region.Absorption,
            F_i: region.Fission,
            N_i: region.Nu,
            x_i: x_i_val
        })
            
    # Step 1: Identify zero constants
    zero_constants = {}
    for eq in boundaries + interfaces:
        if eq.rhs == 0 and len(eq.lhs.free_symbols) == 1:
            # It's of the form Eq(Ci, 0)
            const = list(eq.lhs.free_symbols)[0]
            zero_constants[const] = 0

    # Step 2: Substitute zero constants in the system
    simplified_equations = []
    for eq in fluxes + boundaries + interfaces + powers:
        if eq.lhs not in zero_constants:
            simplified_eq = eq.subs(zero_constants)
            simplified_equations.append(simplified_eq)
            print(f"Substituting {zero_constants} in {eq} gives {simplified_eq}")

    # Display the results
    print("Zero Constants:")
    print(zero_constants)
        
    return simplified_equations

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
        if region == last_region_right or region == last_region_left:
            print(f"The region {i+1} spanning from {region.Start} to {region.End} is a boundary region")
            boundary_cond = obc.outer_boundary_conditions(fluxes[i], x,region, regions)
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
    # Now integrate the flux over the region
    for region in fission_regions:
        index = regions.index(region)
        integrated_flux = sp.integrate(fluxes[index].rhs, (x, region.Start, region.End))
        power = sp.Eq(region.Fission * energy_per_fission * integrated_flux, region.Power)
        powers.append(power)

    ############################################################################################################
    # Check for symmetry
    ############################################################################################################
    symmetry = False
    for i, region in enumerate(regions):
        if region.Symmetry != 0:
            symmetry = True
            sym_reg_index = region.Symmetry - 1
            print(f"Region {i+1} is symmetric to Region {region.Symmetry}")
            
            # Replace with proper known values D, B, L
            x = sp.symbols('x')
            D_i = sp.symbols(f'D_{i+1}', positive=True)
            B_i = sp.symbols(f'Bg_{i+1}', positive=True)
            L_i = sp.symbols(f'L_{i+1}', positive=True)
            C_1 = sp.symbols(f'C_{i*2+1}', positive=True)
            C_2 = sp.symbols(f'C_{i*2+2}', positive=True)
            D_sym = sp.symbols(f'D_{sym_reg_index+1}', positive=True)
            B_sym = sp.symbols(f'Bg_{sym_reg_index+1}', positive=True)
            L_sym = sp.symbols(f'L_{sym_reg_index+1}', positive=True)
            C_1_sym = sp.symbols(f'C_{sym_reg_index*2+1}', positive=True)
            C_2_sym = sp.symbols(f'C_{sym_reg_index*2+2}', positive=True)
            x_interface = sp.symbols(f'x_{i+1}', positive=True) # The interface is at the end of the left region, Region 1 has interface at x_1
            x_sym_interface = sp.symbols(f'x_{sym_reg_index}', positive=True) # The interface is at the end of the left region, Region 3 has interface at x_2
            
            sym_region_symbols = [C_1_sym, C_2_sym]
            
            # Replace in the flux
            fluxes[i] = fluxes[i].subs({
                D_sym: D_i,
                B_sym: B_i,
                L_sym: L_i,
                C_1_sym: C_1,
                C_2_sym: C_2,
                x: x - region.End
            })

            # Replacing in boundaries
            sym_boundary_conditions = [
                cond.subs({
                        D_sym: D_i,
                        B_sym: B_i,
                        L_sym: L_i,
                        C_1_sym: C_1,
                        C_2_sym: C_2,
                        x: x - region.End + regions[sym_reg_index].Start
                    }, evaluate=False)
                for cond in boundaries if any(sym in cond.free_symbols for sym in sym_region_symbols)
            ]

            # Replacing in interfaces
            sym_interface_conditions = [sp.Eq(
                cond.lhs,
                cond.rhs.subs( # Orribile hack to get it working, Force it to be a right hand side
                    {
                        D_sym: D_i,
                        B_sym: B_i,
                        L_sym: L_i,
                        C_1_sym: C_1,
                        C_2_sym: C_2,
                        x_sym_interface: x_interface - region.End + regions[sym_reg_index].Start
                    }
                )
            , evaluate=False)
                for cond in interfaces  if any(sym in cond.free_symbols for sym in sym_region_symbols)
            ]

            

            # Remove old boundary and interface conditions
            # Constants to be removed
            constants_to_remove = {C_1, C_2}
            print(f"Removing constants {constants_to_remove} from the boundary and interface conditions")
            # Filter boundaries
            boundaries = [
                cond for cond in boundaries
                if not any(const in cond.free_symbols for const in constants_to_remove)
            ]

            # Filter interfaces
            interfaces = [
                cond for cond in interfaces
                if not any(const in cond.free_symbols for const in constants_to_remove)
            ]


            # Add the new symmetric boundary and interface conditions
            boundaries += sym_boundary_conditions
            interfaces += sym_interface_conditions
                        
    if symmetry:
        # Get the minimum, non inifite value of Region.Start and the maximum, non infinite value of Region.End
        min_start = min([region.Start for region in regions if region.Start != -sp.oo])
        max_end = max([region.End for region in regions if region.End != sp.oo])
        
        # Get the average of the two values
        avg = (min_start + max_end) / 2
        
        # Check in which region the average lies
        sym_region = None
        for region in regions:
            if region.Start <= avg <= region.End:
                sym_region = region
                break
        
        # Get the index of the symmetric region
        sym_reg_index = regions.index(sym_region)
        
        # New condition states that the first derivative of the flux is zero at the average
        symmetry_conditions = sp.Eq(sp.diff(fluxes[sym_reg_index].rhs, x).subs(x, avg), 0)
        boundaries.append(symmetry_conditions)

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