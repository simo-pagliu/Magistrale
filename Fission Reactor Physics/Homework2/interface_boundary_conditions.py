import sympy as sp

############################################################################################################
# Function to apply interface boundary conditions
############################################################################################################
def interface_boundary_conditions(flux_left, flux_right, x, region_left, region_right, all_regions):
    # Define the region-specific variables for the left region
    i_left = all_regions.index(region_left)
    D_left = sp.symbols(f'D_{i_left+1}', positive=True)
    F_left = sp.symbols(f'F_{i_left+1}', positive=True)
    A_left = sp.symbols(f'A_{i_left+1}', positive=True)
    N_left = sp.symbols(f'N_{i_left+1}', positive=True)
    B_left = sp.symbols(f'Bg_{i_left+1}', positive=True)

    # Define the region-specific variables for the right region
    i_right = all_regions.index(region_right)
    D_right = sp.symbols(f'D_{i_right+1}', positive=True)
    F_right = sp.symbols(f'F_{i_right+1}', positive=True)
    A_right = sp.symbols(f'A_{i_right+1}', positive=True)
    N_right = sp.symbols(f'N_{i_right+1}', positive=True)
    B_right = sp.symbols(f'Bg_{i_right+1}', positive=True)

    ans = []
    
    # Create a new variabel to indicate the point of the interface
    interface = sp.symbols(f'x_{i_left+1}', real=True) # The interface is at the end of the left region
    
    # Continuity of flux at the interface
    
    flux_at_left = flux_left.rhs.subs(x, interface)
    flux_at_right = flux_right.rhs.subs(x, interface)

    continuity_flux = sp.Eq(flux_at_left, flux_at_right)
    ans.append(continuity_flux)
    
    current_left = -D_left * sp.diff(flux_left.rhs, x).subs(x, interface)
    current_right = -D_right * sp.diff(flux_right.rhs, x).subs(x, interface)

    continuity_curr = sp.Eq(current_left, current_right)
    ans.append(continuity_curr)

    return ans
