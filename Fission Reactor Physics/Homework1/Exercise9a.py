import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import nuclei_func as nf
import csv
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
mass_U = 100e6 #t --> g
molar_mass_U = 235 #g/mol
enrichment = 0.02
thermal_power = 3e9 #GW --> W
sigma_f = 585 #b
branching_ratio_Nd = 0.0107
energy_fission = 200.7 * 1.60218e-13 #MeV --> J
half_life_Nd = 1.37*3600 #h --> s
half_life_Pm = 53.1*3600 #h --> s
sigma_abs_Sm = 42000 #b
N_a = 6.022e23 # Avogadro's number

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
# Decay constants
decay_Nd = np.log(2)/half_life_Nd
decay_Pm = np.log(2)/half_life_Pm

# Variables
t = sp.symbols('t', positive=True, real=True)

# Concentrations - function of time
Ur = sp.Function('Ur')(t)
Nd = sp.Function('Nd')(t)
Pm = sp.Function('Pm')(t)
Sm = sp.Function('Sm')(t)
funs = [Ur, Nd, Pm, Sm]

# Fission rate and Capture rate
f = sp.symbols('f', positive=True, real=True)
c = sp.symbols('c', positive=True, real=True)

# Differential Equations
eq_U = sp.Eq(sp.diff(Ur,t), -f)
eq_Nd = sp.Eq(sp.diff(Nd,t), f * branching_ratio_Nd - decay_Nd * Nd)
eq_Pm = sp.Eq(sp.diff(Pm,t), decay_Nd * Nd - decay_Pm * Pm)
eq_Sm = sp.Eq(sp.diff(Sm,t), decay_Pm * Pm - c)
system = [eq_U, eq_Nd, eq_Pm, eq_Sm]

# Initialising solution vectors with initial conditions
U_initial = mass_U * enrichment * N_a / molar_mass_U
solution = [[U_initial], [0], [0], [0]]
time = [0]
############################################################################################################
# Function to solve the system
############################################################################################################
def solving(days, status):
    # time interval
    step = 1000
    t_vals = np.geomspace(0.0001, days*24*3600, num=days*step)
    # initial conditions
    init = {Ur.subs(t,0): solution[0][-1], Nd.subs(t,0): solution[1][-1], Pm.subs(t,0): solution[2][-1], Sm.subs(t,0): solution[3][-1]}
    print(init)
    if status == 1:
        f_r = fission_rate
        c_r = capture_rate
    else:
        f_r = 0
        c_r = 0

    # Solve the system
    sol = sp.dsolve(system, funs, ics=init) 
    sol = [eq.subs(f, f_r).subs(c, c_r) for eq in sol]

    # Evaluate solutions at the time interval
    Ur_temp = [sol[0].rhs.subs(t, t_val) if sol[0].rhs.subs(t, t_val) >= 0 else 0 for t_val in t_vals]
    Nd_temp = [sol[1].rhs.subs(t, t_val) if sol[1].rhs.subs(t, t_val) >= 0 else 0 for t_val in t_vals]
    Pm_temp = [sol[2].rhs.subs(t, t_val) if sol[2].rhs.subs(t, t_val) >= 0 else 0 for t_val in t_vals]
    Sm_temp = [sol[3].rhs.subs(t, t_val) if sol[3].rhs.subs(t, t_val) >= 0 else 0 for t_val in t_vals]

    # Add to the list U_sol the values of U_temp
    return solution[0].extend(Ur_temp), solution[1].extend(Nd_temp), solution[2].extend(Pm_temp), solution[3].extend(Sm_temp), time.extend(t_vals + time[-1])

############################################################################################################
# Solve the system
############################################################################################################
# solving(#number of days, #status: 1 for nominal power, 0 for scrammed)
solving(7, 1)
solving(1, 0)
solving(3, 1)

############################################################################################################
# Save the concentration data to a file for later use in Exercise9b.py
############################################################################################################
csv_file_path = "./Fission Reactor Physics/Homework1/Sol_9.csv"

data = {
    "Time [s]": time,
    "U-235 [atoms]": solution[0],
    "Nd-140 [atoms]": solution[1],
    "Pm-149 [atoms]": solution[2],
    "Sm-149 [atoms]": solution[3]
}

# Save the data to a csv file
with open(csv_file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(data.keys())
    writer.writerows(zip(*data.values()))

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_9.txt", "w") as f:
    f.write(f"{str_1}\n")