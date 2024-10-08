import numpy as np
import sympy as sp

############################################################################################################
# Function to apply boundary condition for outer regions
############################################################################################################
def outer_boundary_conditions(flux, x, region, all_regions, Symmetric):
    # Define the region-specific variables
    i = all_regions.index(region)
    D_i = sp.symbols(f'D_{i+1}', positive=True)
    F_i = sp.symbols(f'F_{i+1}', positive=True)
    A_i = sp.symbols(f'A_{i+1}', positive=True)
    N_i = sp.symbols(f'N_{i+1}', positive=True)
    B_i = sp.symbols(f'Bg_{i+1}', positive=True)
    L_i = sp.symbols(f'L_{i+1}', positive=True)

    ans = []
    
    # Get the correct boundary
    for other_region in all_regions:
        if other_region != region:
            if isinstance(region.End, sp.Symbol) or isinstance(other_region.Start, sp.Symbol): #TO FIX
                pass
            # First check the end of the region
            elif not region.End in [other_region.Start, other_region.End]:
                boundary = region.End
                temp = evaluate_boundary(flux, x, region, i, D_i, F_i, A_i, N_i, B_i, L_i, boundary)  
                for condition in temp:
                    ans.append(condition)

            # Then before checking the start verify if the region is symmetric
            if region.Start == 0 and Symmetric == True:
                print(f"Region {i+1} is symmetric")
                # In this case the condition on 0 is just the derivative@0 = 0
                symmetry_conditions = sp.Eq(sp.diff(flux.rhs, x).subs(x, 0), 0, evaluate=False)
                ans.append(symmetry_conditions)
            
            # If it didn't fall into the first case, check if the start of the region si a boundary
            elif not region.Start in [other_region.Start, other_region.End]:
                boundary = region.Start # This means that it is not an interface 
                temp = evaluate_boundary(flux, x, region, i, D_i, F_i, A_i, N_i, B_i, L_i, boundary)  
                for condition in temp:
                    ans.append(condition)

    return ans

def evaluate_boundary(flux, x, region, i, D_i, F_i, A_i, N_i, B_i, L_i, boundary):
    Extrapolation_Length = abs(boundary) + 0.7/region.Diffusion  
    sign = np.sign(boundary)
    ans = []
    
    print(f"Applying boundary condition at x = {boundary}")

    # Identify the terms in the general solution
    terms = flux.rhs.as_ordered_terms()
    
    # Evaluate the limit
    limit = sp.limit(flux.rhs, x, sign * Extrapolation_Length) # Evaluate the limit at the extrapolation length
    infinity_terms = 0 # Count the number of terms that go to infinity
    
    known_symbols = {x, D_i, F_i, N_i, A_i, B_i, L_i}
    for prop in vars(region).values():
        if isinstance(prop, sp.Basic):
            known_symbols.update(prop.free_symbols)

    # If limit goes to infinity
    if limit.has(sp.oo) or limit.has(-sp.oo):
        # Evaluate each term
        for term in terms:
            limit_term = sp.limit(term, x, sign * Extrapolation_Length)
            # And set to 0 those that go to infinity
            if limit_term.has(sp.oo):
                # known_symbols = {x, D_i, F_i, N_i, A_i, B_i, L_i}
                term_symbols = term.free_symbols
                constant = list(term_symbols - known_symbols)[0]  
                print(f"Term {term} has infinity at x = {boundary}")
                new_condition = sp.Eq(constant, 0, evaluate=False)
                ans.append(new_condition) 
                infinity_terms += 1 # Count the number of terms that go to infinity
            
        # If all terms go to infinity, the constants are not constants
        # so we express them as a function
        if infinity_terms == len(terms):
            C_1 = sp.symbols(f'C_{i*2+1}', positive=True, real=True)
            C_2 = sp.symbols(f'C_{i*2+2}', positive=True, real=True)
            print(f"All terms go to infinity at x = {boundary}")
            # Get the argument of each term
            argument = [term.args[1].args[0] for term in terms][0]
            new_condition = sp.Eq(C_2, C_1*sp.tanh(argument), evaluate=False)
            ans = [new_condition] # Set the ratio as a condition, rewriteing the previous conditions
            print(f"New condition is {new_condition}")
            
    elif limit == 0: # If limit is zero by itself, :D
        print(f"Flux goes to zero at x = {boundary} for any value of the constants")
    else: # If limit is finite, it should be zero
        print(f"Flux goes to {limit} at x = {boundary}")
        new_condition = sp.Eq(limit, 0, evaluate=False)
        ans.append(new_condition)
    return ans