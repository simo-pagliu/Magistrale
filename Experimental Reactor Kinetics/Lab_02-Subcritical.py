########################################################################################
from framework import Measurement as m
from framework import rss

# Data analysis assignments:
# 1) calculate the calibration factor for the fission chamber using a different reference value - DONE
# 2) calculate and compare the integral reactivity worth for the SHIM, REG & TRANS obtained with  different reference values - DONE
# 3) estimate the possible sources of uncertainty and calculate their impact on the CR worth
# 4) comment on the impact of not having the core in a clean state (e.g., which is the information we can extract?)  

# Reference Names for the conditions
cond = [
    "All In", 
    "Shim Out", 
    "Reg Out", 
    "Trans Out"
]

# Known control rod worths
known_CR_w = [
    0.00, #all in
    3.22, #shim
    1.26, #reg
    2.23, #trans
]
########################################################################################

########################################################################################
# Montecarlo simulation results
# Obtained by Serpent simulation
k_mc = [
    m(9.62708E-01, 0.00127), # all in 9.62708E-01 0.00127
    m(9.86959E-01, 0.00036), # shim 9.86959E-01 0.00036
    m(9.74998E-01, 0.00069), # reg  9.74998E-01 0.00069
    m(9.80734E-01, 0.00069)  # trans 9.80734E-01 0.00069
    ]

# Beta values from the simulation
beta_mc = [
    m(0.0073, 0), # all in - 6.82806E-03 0.00588
    m(0.0073, 0), # shim - 6.89188E-03 0.00424 
    m(0.0073, 0), # reg - 6.83157E-03 0.00571 / 2.75349E-06 0.60452
    m(0.0073, 0), # trans - 6.85212E-03 0.00570
]

# Calculate reactivity
rho_mc = [rss(lambda k: (k-1)/k, k_mc_val) for k_mc_val in k_mc]

# Compute Control Rod Worth, in dollars
CR_worth_mc = [rss(lambda rho, beta, rho_0: (rho - rho_0) / beta, rho_mc[i], beta_mc[i], rho_mc[0]) for i in range(0, 4)]

# Print results
print("\033[93mMontecarlo results:\033[0m")
for i in [0,1,2,3]:
    print(f"{cond[i]} → CR worth = {CR_worth_mc[i]} $, interval: {(CR_worth_mc[i].value - CR_worth_mc[i].uncertainty):.2f} ~ {(CR_worth_mc[i].value + CR_worth_mc[i].uncertainty):.2f} $")
print("\n")

Criticality_Reg_estimate = m(1.30212, 0.0321023)
Overestimation = rss(lambda crit_est: (crit_est - 1.26) / 1.26, Criticality_Reg_estimate)
print(f"Overestimation of k based on previous simulation in criticality condition: {Overestimation*100}% \n")

print("\033[93mMontecarlo results + Correction:\033[0m")
for i in [0,1,2,3]:
    Corrected = rss(lambda CR_worth, Overestimation: CR_worth * (1-Overestimation), CR_worth_mc[i], Overestimation)
    print(f"{cond[i]} → CR worth = {Corrected} $, interval: {(Corrected.value - Corrected.uncertainty):.2f} ~ {(Corrected.value + Corrected.uncertainty):.2f} $")
print("\n")

########################################################################################

########################################################################################
# Experimental results
# Fission chamber counting rates
counting_rates = [
    m(0.6290, 0.0177), # all in 
    m(2.5210, 0.0502), # shim
    m(0.8855, 0.0210), # reg
    m(1.4920, 0.0389), # trans
]
# counting_rates = [
#     m(6.76980E-01, 0.03490), # all in 6.76980E-01 0.03490 3.35404E+05 0.03347 
#     m(1.85691E+00, 0.02714), # shim 1.85691E+00 0.02714 9.67210E+05 0.02897  
#     m(1.00863E+00, 0.02821), # reg  1.00863E+00 0.02821  4.96718E+05 0.02730 
#     m(1.19178E+00, 0.03302), # trans 1.19178E+00 0.03302 6.62469E+05 0.03332 
# ]

# We have to find the calibration factor
calib_factors = []
for i in [1, 2, 3]:
    calib_gamma = counting_rates[i] / counting_rates[0]
    calib_known_cr_worth = known_CR_w[i] * beta_mc[i] # from reactor period method
    calib_reactivity = (-(calib_known_cr_worth-1)-((calib_known_cr_worth-1)**2+4*calib_known_cr_worth*calib_gamma/(calib_gamma-1)).sqrt())/2 # MEH
    calib_k = rss(lambda rho: 1 / (1 - rho), calib_reactivity)
    calib_subcritical_multiplication_factor = rss(lambda k: 1 / (1 - k), calib_k)
    calib = counting_rates[0] / calib_subcritical_multiplication_factor
    calib_factors.append(calib)
    print(f"Calibration factor by using {cond[i]} as a reference: {calib}")

for j, alpha in enumerate(calib_factors):
    rho_exp_vals = []
    print(f"\nExperimental results - Calibration on {cond[j+1]}:")
    # Calculate k values
    # By estimation from the counting rates
    sub_crit_k = counting_rates[0] / alpha
    k = rss(lambda m: (m - 1) / m, sub_crit_k)
    rho_exp_0 = rss(lambda k: (k - 1) / k, k)

    for i in [1, 2, 3]:
        sub_crit_k = counting_rates[i] / alpha
        print(f"Subcritical multiplication factor for {cond[i]}: {sub_crit_k}")
        k = rss(lambda m: (m - 1) / m, sub_crit_k)
        print(f"K for {cond[i]}: {k}")
        rho_exp = rss(lambda k: (k - 1) / k, k)
        print(f"Reactivity for {cond[i]}: {rho_exp}")
        CR_worth_exp = ((rho_exp - rho_exp_0) / beta_mc[i]) # MEH
        print(f"{cond[i]} → CR worth = {CR_worth_exp} $")
########################################################################################

########################################################################################
# For reference, the "official" results for the CR worth are:
# Shim: 3.22$
# Reg: 1.26$
# Trans: 2.23$
# For the shim and the reg it looks like that using
# set pop 100000 500 20 
# in the serpent code is enough to get a decent result
# the error on the value of K is ~ +- 0.0002
# unfortunately the transient needs much more accuracy
# this is beacuse the difference in the reactivity is much smaller
########################################################################################

import numpy as np
import matplotlib.pyplot as plt


 
raji_convertion_x = [6.539923954372626, 17.00380228136882, 27.832699619771866, 43.89353612167302]
raji_convertion_y = [1.6954314720812182, 4.558375634517766, 7.786802030456853, 12.416243654822335]
# linear relation between x and y create convertion factor
raji_convertion = np.polyfit(raji_convertion_x, raji_convertion_y, 1) # m and q

import csv
# set current directory as working directory
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Open and read the CSV file
geiger1964_x = []
geiger1964_y = []
with open("geiger1964.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header if needed
    for row in reader:
        x, y = map(float, row)  # Convert values to floats
        geiger1964_x.append(x)
        geiger1964_y.append(y)

# for x, y in zip(geiger1964_x, geiger1964_y):
#     print(f"{x:.2f} {y:.2f}")

raju1964_x = []
raju1964_y = []
with open("raju1964.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header if needed
    for row in reader:
        x, y = map(float, row)  # Convert values to floats
        raju1964_x.append(x)
        raju1964_y.append(y)
raju1964_x = np.array(raju1964_x) * raji_convertion[0] + raji_convertion[1]
#normalize y data
raju1964_y = np.array(raju1964_y) / np.max(raju1964_y)

thompson1956_x = []
thompson1956_y = []
with open("thompson1956.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header if needed
    for row in reader:
        x, y = map(float, row)  # Convert values to floats
        thompson1956_x.append(x)
        thompson1956_y.append(y)
#normalize y data
#thompson1956_y = np.array(thompson1956_y) / np.max(thompson1956_y)


# Energy values represent the upper bounds of the bins
energy_bounds = np.array([0.1, 0.75, 1.25, 2.7, 3.7, 5.3, 5.8, 6.7, 8.3, 8.7, 11.7])
# Corresponding weights (normalized counts or probabilities)
y_values = np.array([0, 0, 0.29, 0.53, 0.75, 0.94, 0.77, 0.59, 0.40, 0.26, 0.09])
# y_values *= 0.63  # Adjust weights by scaling factor
# y_values[1] = 0.37  # Update based on the paper's statement

# Calculate bin widths and bin centers
bin_widths = np.diff(energy_bounds)
bin_centers = energy_bounds[:-1] + bin_widths / 2

# Plot histogram
plt.bar(bin_centers, y_values[:-1], width=bin_widths, align='center', edgecolor='black')
plt.xlabel('Energy [MeV]')
plt.ylabel('Weight (Normalized)')
plt.title('Energy Distribution')


#plot geiger data
plt.scatter(geiger1964_x, geiger1964_y, label="Geiger 1964")

#plot raju data
#plt.scatter(raju1964_x, raju1964_y, label="Raju 1964")

#plot thompson data
plt.scatter(thompson1956_x, thompson1956_y, label="Thompson 1956")
plt.legend()
plt.show()
# Calculate the average energy using the weights (y_values)
# Weighted average considers bin centers and corresponding weights
average_energy = np.sum(bin_centers * y_values[:-1]) / np.sum(y_values[:-1])
print(f"Average Energy: {average_energy:.2f} MeV")


