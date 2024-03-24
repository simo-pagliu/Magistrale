import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy.solvers.ode.systems import dsolve_system
import nuclei_func as nf
############################################################################################################
# Exercise 9
############################################################################################################
# Other than 135Xe, another important fission product in terms of neutron absorption is 149Sm, which has the following decay chain:
# U-235 -1.07%-> Nd-140 -1.37h-> Pm-149 -53.1h-> Sm-149 -absorption-> Sm-150
# Use the following data to compute the reaction rate: mass U = 100 t, enrichment = 0.02, thermal power = 3 GW,  = 585 b, 
# energy per fission = 200.7 MeV and the data reported in figure. 
# From the decay chain listed above, compute the Promethium and Samarium concentration (initial concentration equal to zero) for:
#     • Seven days of reactor operation at nominal power.
#     • After 7 days, shutdown at zero power for 1 day.
#     • Reactor restart at nominal power and operation for 3 days.
# for this one we an use sympy to solve the system of equations
# Data:
mass_U = 100 #t
molar_mass_U = 235 #g/mol
enrichment = 0.02
thermal_power = 3e9 #GW --> W
sigma_f = 585 #b
branching_ratio_Nd = 0.0107
energy_fission = 200.7 * 1.60218e-13 #MeV --> J
half_life_Nd = 1.37 #h
half_life_Pm = 53.1 #h
sigma_abs_Sm = 42e3 #b
N_a = 6.022e23 # Avogadro's number
barn = 1e-24 # cm2

############################################################################################################
# Compute the reaction rate
############################################################################################################
# fission rate
fission_rate = thermal_power / energy_fission

# neutron flux
Sigma_fiss_U = nf.macro(sigma_f, 19, 235)
flux = fission_rate / Sigma_fiss_U

# reaction rate
Sigma_abs_Sm = nf.macro(sigma_abs_Sm, 7.52, 149)
capture_rate = flux * Sigma_abs_Sm
str_1 = f"Reaction rate of Sm-149 (absorption): {capture_rate:.4e} "
print(str_1)

############################################################################################################
# System of differential equations
############################################################################################################
# decay constants
decay_Nd = np.log(2)/half_life_Nd
decay_Pm = np.log(2)/half_life_Pm

# concentrations
t = sp.symbols('t', positive=True, real=True)
Ur = sp.Function('Ur')(t)
Nd = sp.Function('Nd')(t)
Pm = sp.Function('Pm')(t)
Sm = sp.Function('Sm')(t)
funs = [Ur, Nd, Pm, Sm]

# fission rate and capture rate
f = sp.symbols('f', positive=True, real=True)
c = sp.symbols('c', positive=True, real=True)

# equations
eq_U = sp.Eq(sp.diff(Ur,t), -f)
eq_Nd = sp.Eq(sp.diff(Nd,t), f * branching_ratio_Nd - decay_Nd * Nd)
eq_Pm = sp.Eq(sp.diff(Pm,t), decay_Nd * Nd - decay_Pm * Pm)
eq_Sm = sp.Eq(sp.diff(Sm,t), decay_Pm * Pm - c)
system = [eq_U, eq_Nd, eq_Pm, eq_Sm]

# initial conditions
U_Sol = [mass_U * enrichment * N_a / molar_mass_U]
Nd_Sol = [0]
Pm_Sol = [0]
Sm_Sol = [0]

############################################################################################################
# Function to solve the system
############################################################################################################
def solving(t_vals, status):
    # initial conditions
    init = {Ur.subs(t,0): U_Sol[-1], Nd.subs(t,0): Nd_Sol[-1], Pm.subs(t,0): Pm_Sol[-1], Sm.subs(t,0): Sm_Sol[-1]}
    if status == 1:
        f_r = fission_rate
        c_r = capture_rate
    else:
        f_r = 0
        c_r = 0

    sys = [eq.subs(f, f_r).subs(c, c_r) for eq in system]
    print(sys)

    sol = sp.dsolve(sys, ics=init) 
    print(sol)

    U_Sol.append(sol[0].rhs.subs(t, t_vals))
    Nd_Sol.append(sol[1].rhs.subs(t, t_vals))
    Pm_Sol.append(sol[2].rhs.subs(t, t_vals))
    Sm_Sol.append(sol[3].rhs.subs(t, t_vals))

############################################################################################################
# Solve the system
############################################################################################################
# 7 days on
t_vals_1 = np.linspace(0, 7*24*3600, 100)
solving(t_vals_1, system, 1)

# off 1 day
t_vals_2 = np.linspace(0, 1*24*3600, 100)
solving(t_vals_2, system, 0)

# back on for 3 days
t_vals_3 = np.linspace(0, 3*24*3600, 100)
solving(t_vals_3, system, 1)

# time 
t_vals = [t_vals_1, t_vals_2, t_vals_3]

############################################################################################################
# Plot the concentrations
############################################################################################################
#plot the concentrations
plt.figure()
plt.plot(t_vals, U_Sol, label='U-235')
plt.plot(t_vals, Nd_Sol, label='Nd-140')
plt.plot(t_vals, Pm_Sol, label='Pm-149')
plt.plot(t_vals, Sm_Sol, label='Sm-149')
plt.xlabel("Time [s]")
plt.ylabel("Concentration [atoms]")
plt.title("Concentration of isotopes over time")
plt.legend()
plt.grid()
plt.show()

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_9.txt", "w") as f:
    f.write("\n")