import sympy as sp

############################################################################################################
# Define symbols
############################################################################################################
x = sp.symbols('x')
D = sp.symbols('D', positive=True)  # Diffusion coefficient
C = sp.symbols('C', positive=True)  # Capture Cross Section
F = sp.symbols('F', positive=True)  # Nu * Fission Cross Section
A = F + C  # Absorption Cross Section

############################################################################################################
# Define the Region class
############################################################################################################
class Region:
    def __init__(self, Diff, Abs, Fiss, Temp, Widt, composition):
        self.Diff = Diff  # Diffusion coefficient
        self.Abs = Abs  # Source term
        self.Fiss = Fiss  # Sigma Absorption / Diffusion
        self.Temp = Temp  # Temperature of the region
        self.Widt = Widt  # Width of the region
        self.composition = composition  # Composition of the region

############################################################################################################
# INPUT EXAMPLE
############################################################################################################
Core = Region(1, 320, 100, 60, 50, {'H': 2, 'O': 1, 'U-235': 1})
Reflector = Region(1, 3000, 0, 60, sp.oo, {'H': 2, 'O': 1})
regions = [Core, Reflector]

############################################################################################################
# Define the diffusion equations for each region
############################################################################################################
def define_diffusion_equations(regions):
    global x, D, A, F      
    
    equations = []
    fluxes = []
    for i, region in enumerate(regions):

        # Define the flux function
        Flux = sp.Function(f'phi_{i+1}', real=True)(x)
        if region.Fiss == 0:
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) - (A/D) * Flux, 0)
        else:
            diff_eq = sp.Eq(sp.diff(Flux, x, 2) + ((A - F)/D) * Flux, 0)
        
                
        # Generate unique constants for each region
        C1, C2 = sp.symbols(f'C{i*2+1} C{i*2+2}', positive=True)
        
        print(diff_eq)
        flux_sol = sp.dsolve(diff_eq, Flux)
        
        # Substitute the constants into the solution
        flux_sol = flux_sol.subs({sp.symbols('C1'): C1, sp.symbols('C2'): C2})
        
        if region.Widt == sp.oo:
            flux_sol = apply_boundary_condition(flux_sol, x)
        equations.append(diff_eq)
        fluxes.append(flux_sol)
        
    return equations, fluxes

############################################################################################################
# Function to apply boundary condition for infinite regions
############################################################################################################
def apply_boundary_condition(flux, x):
    # Identify the terms in the general solution
    terms = flux.rhs.as_ordered_terms()  # Divide the expression into terms
    
    # Determine which term goes to infinity as x -> infinity
    new_terms = []
    for term in terms:
        print(term)
        limit_term = sp.limit(term, x, sp.oo)  # Calculate the limit of the term as x -> infinity
        print(limit_term)
        if limit_term.has(sp.oo):  # Check if the limit is infinity (any expression that contains oo)
            term = 0  # If the limit is infinity, the term is set to zero
        new_terms.append(term)  # Add the term to the new list of terms
            
    flux = sp.Eq(flux.lhs, sum(new_terms))  # Reconstruct the expression with the new terms
    return flux

############################################################################################################
# PRINT EQUATIONS FOR DEBUGGING
############################################################################################################
equations, fluxes = define_diffusion_equations(regions)

print('Diffusion equations:')
for eq in equations:
    print(eq)

print('\nFluxes:')
for flux in fluxes:
    print(flux)
    
    
# TO DO: 
# Boundary conditions
# It should add interface conditions between regions by itself
# then we see how many conditions are still needed to solve the system
# It then has to compute the cross sections based on the composition
# and then from these and the temperature compute all the needed coefficients