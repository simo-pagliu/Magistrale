import numpy as np
import matplotlib.pyplot as plt
import json
#########################################
# Montecarlo homework
# bla bla bla
#########################################

##################################################
# Initialize simulation parameters
##################################################

#fetch json
with open('MC_Proj.json') as f:
    data = json.load(f)

# Assign variables from JSON data
for key, value in data.items():
    globals()[key] = value

# Now you can use the variables directly
print(stories)
print(mission_time)
print(time_steps)
print(failure_rate)
print(repair_rate)

##################################################
# Define functions
##################################################

