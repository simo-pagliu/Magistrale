# See notes for the exercise solution
# Here i may try to generalize the request

# Compute the multiplication factor k_inf 
# For a homogeneous reactor 
# Given the composition of Fuel and Other materials (hadles more elements)

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

##THERMAL UTILIZATION FACTOR
def f(materials, fuel_percentage):
    temp_1 = 0
    temp_2 = 0
    for kk in range(len(fuel)):
        temp_1 =+ fuel_percentage * fuel[kk]["Percentage"] * fuel[kk]["Absorption_CS"]

    for jj in range(len(materials)):
        temp_2 =+ materials[jj]["Percentage"] * materials[jj]["Absorption_CS"] 

    f = temp_1/(temp_1 + temp_2)
    
    return f

#nu, average number of neutrons per fission
def nu(Energy):
    nu_value = 2.432 + 0.066*Energy*1e-6 #average number of neutrons per fission in MeV
    return nu_value

## NEUTRONS PRODUCED BY FISSION PER NEUTRON ABSORBED IN FUEL
def mu(fuel):
    temp_1 = 0
    temp_2 = 0
    for ii in range(len(fuel)):
        temp_1 =+ fuel[ii]["Nu"] * fuel[ii]["Percentage"] * fuel[ii]["Fission_CS"]
        temp_2 =+ fuel[ii]["Percentage"]*fuel[ii]["Absorption_CS"]
    mu_value = temp_1/temp_2
    return mu_value

## DON'T KNOW THESE; JUST SET THEM TO ONE FOR THE TIME BEING
eta = 1 #number of thermal and fast fissions over thermal fissions only
p = 1 #probability of not getting absorbed during resonance
P_nl_th = 0.5 #probability of not getting absorbed during thermal neutron scattering
P_nl_f = 0.5 #probability of not getting absorbed during fast neutron scattering
Energy_Eval = 25e-3 #THERMAL EVALUATION eV energy at which we evaluate cross sections [eV]

## FUEL COMPOSITION
fuel = []
fuel.append({"Elements": 'U-235', "Percentage": 5, "Nu": nu(Energy_Eval), "Fission_CS": 590, "Absorption_CS": 590+100})
fuel.append({"Elements": 'U-238', "Percentage": 94, "Nu": nu(Energy_Eval), "Fission_CS": 0, "Absorption_CS": 2.73})
fuel.append({"Elements": 'U-233', "Percentage": 1, "Nu": nu(Energy_Eval), "Fission_CS": 523, "Absorption_CS": 523+49})

## FUEL PERCENTAGE OVER TOTAL 
fuel_percentage = 1.2e-3 #percentage of fuel over the total amount of materials

## REACTOR COMPOSITION
materials = []
materials.append({"Material": 'H2O', "Percentage": 0.7, "Absorption_CS": 0.66}) #FOR BETTER RESULTS SUBTRACT THE FUEL PERCENTAGE FROM ONE OF THESE
materials.append({"Material": 'Fe', "Percentage": 0.3, "Absorption_CS": 2.62})



## MULTIPLICATION FACTOR
k_inf = eta*p*mu(fuel)*f(materials, fuel_percentage)*(P_nl_th + P_nl_f)
print(k_inf)



