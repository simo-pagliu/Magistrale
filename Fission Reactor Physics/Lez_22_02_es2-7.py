#import packages
import math
import numpy as np
import sympy

#constants
Intensity = 1e12 # n/cm2 sec
cross_sec_tot = 4 #barn

mean_time_before_interaction = 1 / (Intensity * cross_sec_tot*1e-24)
#print mean_time_before_interaction in scientific notation
print(f"{mean_time_before_interaction:.2e}")