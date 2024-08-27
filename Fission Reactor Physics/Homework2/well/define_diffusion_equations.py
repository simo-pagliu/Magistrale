import sympy as sp

############################################################################################################
# Define the diffusion equations for each region
############################################################################################################
def define_diffusion_equations(regions, x):   
    equations = []
    fluxes = []
    for i, region in enumerate(regions):
        # Define the region-specific variables
        D_i = sp.symbols(f'D_{i+1}', positive=True)
        F_i = sp.symbols(f'F_{i+1}', positive=True)
        A_i = sp.symbols(f'A_{i+1}', positive=True)
        N_i = sp.symbols(f'N_{i+1}', positive=True)
        B_i = sp.symbols(f'Bg_{i+1}', positive=True)
        L_i = sp.symbols(f'L_{i+1}', positive=True)

        # Define the flux function
        Flux = sp.Function(f'phi_{i+1}', real=True)(x)
        if region.Fission == 0:
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) - (1/L_i**2) * Flux, 0)
        else:
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) + (B_i**2) * Flux, 0)
        
        # Generate unique constants for each region
        C1, C2 = sp.symbols(f'C_{i*2+1} C_{i*2+2}', real=True)
        
        # Solve the differential equation
        flux_sol = sp.dsolve(diff_eq, Flux)
        
        # Substitute the constants into the solution
        flux_sol = flux_sol.subs({sp.symbols('C1'): C1, sp.symbols('C2'): C2}) 

        if region.Composition == 'h':
            print(f"Region {i+1} has sinh and cosh")
            C1, C2 = sp.symbols(f'C_{i*2+1} C_{i*2+2}', function=True)
            flux_sol = sp.Eq(Flux, C1*sp.sinh(-x/L_i) + C2*sp.cosh(-x/L_i))

        # Translate the solution to the correct position
        if region.Start == -sp.oo:
            flux_sol = flux_sol.subs(x, x - region.End)
        else:
            flux_sol = flux_sol.subs(x, x - region.Start)

        equations.append(diff_eq)
        fluxes.append(flux_sol)
        
    return equations, fluxes