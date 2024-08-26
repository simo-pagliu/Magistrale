import sympy as sp
def i():
    ############################################################################################################
    # Define symbols
    ############################################################################################################
    x = sp.symbols('x')
    D = sp.symbols('D', positive=True)  # Diffusion coefficient
    C = sp.symbols('C', positive=True)  # Capture Cross Section
    F = sp.symbols('F', positive=True)  # Fission Cross Section
    N = sp.symbols('N', positive=True)  # Number of Neutrons per Fission
    A = F + C  # Absorption Cross Section

    ############################################################################################################
    # Define the Region class
    ############################################################################################################
    class Region:
        def __init__(self, Diff, Abs, Fiss, Nu, Temp, Pos1, Pos2, composition):
            self.Diffusion = Diff  # Diffusion coefficient
            self.Absorption = Abs  # Source term
            self.Fission = Fiss  # Sigma Fission
            self.Nu = Nu  # Number of Neutrons per Fission
            self.Temperature = Temp  # Temperature of the region
            self.Start = Pos1 # Starting Position of the region
            self.End = Pos2  # Ending Position of the region
            self.Composition = composition  # Composition of the region

    return x, D, C, F, N, A, Region