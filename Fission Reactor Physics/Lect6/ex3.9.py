import sympy as sp

t = sp.symbols('t', positive=True, real=True) #define the variable and its conditions
N_t = sp.Function('N_t')(t) #define the number of atoms as a function of time
k = sp.symbols('k', positive=True, real=True) #define the multiplication factor
l = sp.symbols('l', positive=True, real=True) #define the neutron lifetime
S_o = sp.symbols('S_o', positive=True, real=True) #define the source term
#S_o = sp.Function('S_o')(t) #define the source term as a function of time

Eq = sp.Eq(N_t.diff(t), (k-1)/l * N_t + S_o) #define the differential equation

print(Eq)

Sol = sp.dsolve(Eq, N_t, ics = {N_t.subs(t,0): 0}, simplify=True) #solve the differential equation
Sol = Sol.doit() #evaluate the solution
print(sp.latex(Sol))