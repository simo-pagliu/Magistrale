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
    m(0.96870, 0.00418), # all in
    m(0.99169, 0.00159), # shim
    m(0.96415, 0.00491), # reg
    m(0.98287, 0.00406)  # trans
    ]

# Beta values from the simulation
beta_mc = [
    m(0.00731845, 0.00000275), # all in
    m(0.00726903, 0.00000279), # shim 
    m(0.00731473, 0.00000282), # reg 
    m(0.00732162, 0.00000271), # trans 
]

# Calculate reactivity
rho_mc = [rss(lambda k: (k-1)/k, k_mc_val) for k_mc_val in k_mc]

# Compute Control Rod Worth, in dollars
CR_worth_mc = [rss(lambda rho, beta, rho_0: (rho - rho_0) / beta, rho_mc[i], beta_mc[i], rho_mc[0]) for i in range(0, 4)]

# Print results
print("Montecarlo results:")
for i in [1,2,3]:
    print(f"{cond[i]} → CR worth = {CR_worth_mc[i]} $")
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
        k = rss(lambda m: (m - 1) / m, sub_crit_k)
        rho_exp = rss(lambda k: (k - 1) / k, k)
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