import numpy as np
import sympy as sp

############################################################################################################
# Function to apply boundary condition for outer regions
############################################################################################################
def outer_boundary_conditions(flux, x, region, all_regions):
    # Define the region-specific variables
    i = all_regions.index(region)
    D_i = sp.symbols(f'D_{i+1}', positive=True)
    F_i = sp.symbols(f'F_{i+1}', positive=True)
    A_i = sp.symbols(f'A_{i+1}', positive=True)
    N_i = sp.symbols(f'N_{i+1}', positive=True)
    B_i = sp.symbols(f'Bg_{i+1}', positive=True)
    L_i = sp.symbols(f'L_{i+1}', positive=True)
    
    # Get the correct boundary
    start_present = False
    for other_region in all_regions:
        if other_region != region:
            if region.Start in [other_region.Start, other_region.End]:
                start_present = True
    
    if not start_present:
        boundary = region.Start
    else:
        boundary = region.End

    Extrapolation_Length = abs(boundary) + 0.7/region.Diffusion  
    sign = np.sign(boundary)
    ans = []
    
    print(f"Applying boundary condition at x = {boundary}")

    # Identify the terms in the general solution
    terms = flux.rhs.as_ordered_terms()
    
    # Evaluate the limit
    limit = sp.limit(flux.rhs, x, sign * Extrapolation_Length) # Evaluate the limit at the extrapolation length
    infinity_terms = 0 # Count the number of terms that go to infinity
    
    # If limit goes to infinity
    if limit.has(sp.oo) or limit.has(-sp.oo):
        # Evaluate each term
        for term in terms:
            limit_term = sp.limit(term, x, sign * Extrapolation_Length)
            # And set to 0 those that go to infinity
            if limit_term.has(sp.oo):
                known_symbols = {x, D_i, F_i, N_i, A_i, B_i, L_i}
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