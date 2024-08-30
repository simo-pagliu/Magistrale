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
mass_U = 1e8 #t --> g
molar_mass_U = 235 #g/mol
enrichment = 0.02
thermal_power = 3e9 #GW --> W
sigma_f = 585e-24 #b
branching_ratio_Nd = 0.0108
energy_fission = 200.7 * 1.60218e-13 #MeV --> J
half_life_Nd = 1.73*3600 #h --> s
half_life_Pm = 53.1*3600 #h --> s
sigma_abs_Sm = 42000e-24 #b
N_a = 6.022e23 # Avogadro's number
density_U = mass_U*enrichment*(N_a/molar_mass_U)

############################################################################################################
# Compute the reaction rate
############################################################################################################

# neutron flux
flux=thermal_power/(sigma_f*energy_fission*density_U)
Sigma_fiss_U = sigma_f * density_U
print("Flux", flux)
rate_fission=sigma_f*density_U*flux

############################################################################################################
# Ask if you want to solve the system or if you want to use a previously solved system and just plot 
############################################################################################################
print("\033[93mWARNING: Solving this system of equation through sympy might take its time; \n if you have already run this script once there should be a .csv file with the solution and I can just plot the result\033[0m")
print("Do you want to Solve (s) or try to Plot (p) (s/p)?")
answer = input()
if answer == "s":
    pass
elif answer == "p":
    exec(open("./Fission Reactor Physics/Homework1/Exercise9b.py").read())
    exit()

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

# Differential Equations
eq_U = sp.Eq(sp.diff(Ur,t), rate_fission)
eq_U_off = sp.Eq(sp.diff(Ur,t), 0)

eq_Nd = sp.Eq(sp.diff(Nd,t), rate_fission * branching_ratio_Nd - decay_Nd * Nd)
eq_Nd_off = sp.Eq(sp.diff(Nd,t), - decay_Nd * Nd)

eq_Pm = sp.Eq(sp.diff(Pm,t), decay_Nd * Nd - decay_Pm * Pm)

eq_Sm = sp.Eq(sp.diff(Sm,t), decay_Pm * Pm - flux * sigma_abs_Sm * Sm)
eq_Sm_off = sp.Eq(sp.diff(Sm,t), decay_Pm * Pm)

system = [eq_U, eq_Nd, eq_Pm, eq_Sm]
system_off = [eq_U_off, eq_Nd_off, eq_Pm, eq_Sm_off]

# Initialising solution vectors with initial conditions
U_initial = mass_U * enrichment * N_a / molar_mass_U
solution = [[U_initial], [0], [0], [0]]
time = [0]
############################################################################################################
# Function to solve the system
############################################################################################################
def solving(days, system):
    # time interval
    step = 1000
    t_vals = np.geomspace(0.0001, days*24*3600, num=days*step)
    # initial conditions
    init = {Ur.subs(t,0): solution[0][-1], Nd.subs(t,0): solution[1][-1], Pm.subs(t,0): solution[2][-1], Sm.subs(t,0): solution[3][-1]}
    print(init)

    # Solve the system
    sol = sp.dsolve(system, funs, ics=init)     

    print("Solution", sol)

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
# solving(#number of days, system to solve)
solving(7, system)
solving(1, system_off)
solving(3, system)

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
# Ask if you want to exec file Exercise9b.py to plot
############################################################################################################
print("Do you want to plot the results? (y/n)")
answer = input()
if answer == "y":
    exec(open("./Fission Reactor Physics/Homework1/Exercise9b.py").read())