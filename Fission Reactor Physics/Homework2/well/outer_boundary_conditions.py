import numpy as np
import sympy as sp

############################################################################################################
# Function to apply boundary condition for outer regions
############################################################################################################
def outer_boundary_conditions(flux, x, D, F, N, A, B, region, all_regions):
    
    # Get the correct boundary
    # Iterate over all other regions
    start_present = False
    for other_region in all_regions:
        if other_region != region:
            # Check if the start and end of the current region are present in the other region
            if region.Start in [other_region.Start, other_region.End]:
                start_present = True
    
    # If the start of the current region is not present in any other region, use it as the boundary
    if not start_present:
        boundary = region.Start
    else: # Otherwise, use the end of the current region as the boundary
        boundary = region.End

    # Extrapolation Length
    Extrapolation_Length = abs(boundary) + 0.7/region.Diffusion  # Extrapolation length for the boundary condition

    # Sign of the limit = sign of the boundary
    sign = np.sign(boundary)

    # Determine which term goes to infinity as x -> infinity
    ans = []
    limit = 0
    # Identify the terms in the general solution
    terms = flux.rhs.as_ordered_terms()  # Divide the expression into terms
    for term in terms:
        limit_term = sp.limit(term, x, sign * Extrapolation_Length)  # Calculate the limit of the term as x -> infinity
        limit = limit + limit_term
        if limit_term.has(sp.oo):  # Check if the limit is infinity (any expression that contains oo)
            # Define the known symbols
            known_symbols = {x, D, F, N, A, B}

            # Get the symbols in the term
            term_symbols = term.free_symbols

            # Subtract the known symbols from the term symbols to get the integration constant
            constant = term_symbols - known_symbols
            constant = list(constant)[0]  # Extract the constant symbol

            if term.subs(constant,0) == 0:  # Check if the term is zero when the constant is zero
                # The new condition is that the constant is set to zero
                new_condition = sp.Eq(constant, 0, evaluate=False)
                ans.append(new_condition)
                
    # If no terms go to infinity, consider solving the equation directly
    if not ans:
        new_condition = sp.solve(limit)
        print("Boundary condition is non trivial as nothing goes to zero:", new_condition)
        ans.append(new_condition)

    return ans
