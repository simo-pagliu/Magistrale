import sympy as sp
############################################################################################################
# Define the diffusion equations for each region
############################################################################################################
def define_diffusion_equations(regions, x, D, F, N, A, B):   

    equations = []
    fluxes = []
    for i, region in enumerate(regions):

        # Define the flux function
        Flux = sp.Function(f'phi_{i+1}', real=True)(x)
        if region.Fission == 0:
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) - (A/D) * Flux, 0)
        else:
            B = sp.symbols(f'Bg_{i+1}', positive=True)
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) + (B**2) * Flux, 0)
        
                
        # Generate unique constants for each region
        C1, C2 = sp.symbols(f'C{i*2+1} C{i*2+2}', positive=True)
        
        
        # Solve the differential equation
        flux_sol = sp.dsolve(diff_eq, Flux)
        
        # Substitute the constants into the solution
        flux_sol = flux_sol.subs({sp.symbols('C1'): C1, sp.symbols('C2'): C2})

        # Translate the solution to the correct position
        if region.Start == -sp.oo:
            flux_sol = flux_sol.subs(x, x - region.End)
        else:
            flux_sol = flux_sol.subs(x, x - region.Start)

        equations.append(diff_eq)
        fluxes.append(flux_sol)
        
    return equations, fluxes