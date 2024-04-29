import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 3
############################################################################################################
# How many parts per million of boron must be dissolved in water at room temperature to double its absorption cross section for thermal neutrons? 
# Consider two different cases:
#     • All boron is 10B with  b.
#     • Boron is present with its isotopic composition:
#           B-10   19.9 %  3837 b
#           B-11   80.1 %  0.005 b

sigma_B10 = 3837 # b
sigma_B11 = 0.005 # b
# isotope composition
x_mix= 0.199 # 19.9% of B-10
# convert to molar fraction
#x_mix = nf.w2mol([x_mix, 1-x_mix], [10, 11])[0]

sigma_O = 0.0001709 # b
sigma_H = 0.33467 # b
sigma_water = nf.mixture([sigma_H, sigma_O], [2, 1],'normalize')*3

#I used this just to get the expression for x
# import sympy as sp
# x = sp.symbols('x')
# sigma_water = sp.symbols('sigma_water')
# sigma_B = sp.symbols('sigma_B')
# eq = sp.Eq((1-x)*sigma_water + x*sigma_B, 2*sigma_water)
# sol = sp.solve(eq, x)
# print(sol)

############################################################################################################
# Case in which all Boron is B10
############################################################################################################
Sol_1 = sigma_water/(sigma_B10 - sigma_water)
Sol_1 *= 1e6 # convert to ppm
print(f"In case it's all B-10: {Sol_1:.2f} PPM") 

############################################################################################################
# Case in which Boron is a mixture of B10 and B11
############################################################################################################
sigma_B = nf.mixture([sigma_B10, sigma_B11], [x_mix, 1-x_mix])
#print(sigma_B)
Sol_2 = sigma_water/(sigma_B - sigma_water)
Sol_2 *= 1e6 # convert to ppm
print(f"In case is a mix of B-10 and B-11: {Sol_2:.2f} PPM")

############################################################################################################
# Save solution to a file
############################################################################################################
with open(".\Fission Reactor Physics\Homework1\Sol_3.txt", "w") as f:
    f.write(f"Case 1, all boron in B-10: {Sol_1:.2f} PPM\n")
    f.write(f"Case 2, boron is a mix of B-10 and B-11: {Sol_2:.2f} PPM\n")
