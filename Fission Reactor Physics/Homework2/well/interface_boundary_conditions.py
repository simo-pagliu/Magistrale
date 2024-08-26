import sympy as sp
############################################################################################################
# Function to apply interface boundary conditions
############################################################################################################
def interface_boundary_conditions(flux1, flux2, x, D, F, N, A, region1, region2):
    # Continuity of flux
    flux_1 = flux1.rhs.subs(x, region1.End)
    flux_1 = flux_1.subs({D: region1.Diffusion, A: region1.Absorption, F: region1.Fission, N: region1.Nu})
    flux_2 = flux2.rhs.subs(x, region2.Start)
    flux_2 = flux_2.subs({D: region2.Diffusion, A: region2.Absorption, F: region2.Fission, N: region2.Nu})
    continuity_flux = sp.Eq(flux_1, flux_2)

    # Continuity of current
    current_1 = -region1.Diffusion * sp.diff(flux1.rhs, x).subs(x, region1.End)
    current_1 = current_1.subs({D: region1.Diffusion, A: region1.Absorption, F: region1.Fission, N: region1.Nu})
    current_2 = -region2.Diffusion * sp.diff(flux2.rhs, x).subs(x, region2.Start)
    current_2 = current_2.subs({D: region2.Diffusion, A: region2.Absorption, F: region2.Fission, N: region2.Nu})
    continuity_curr = sp.Eq(current_1, current_2)

    return [continuity_flux, continuity_curr]