import numpy as np
import matplotlib.pyplot as plt
#########################################
# Exercise 2.1
# This script simulates the availability of a system over time using Monte Carlo simulation.
#########################################

##################################################
# Initialize simulation parameters
##################################################
stories = 100000 # Set the number of Monte Carlo trials to simulate. 
mission_time = 1000 # Set the mission time in hours.
time_steps = 1000 # Set the number of time steps to discretize the mission time.
time_axis = np.linspace(0, mission_time, time_steps) # Create a time axis from 0 to mission_time.
time_step = time_axis[1] - time_axis[0] # Calculate the time step size.
# System parameters
failure_rate = 3e-3 # Define the failure rate of the system.
repair_rate = 25e-3 # Define the repair rate.

##################################################
# Perform Monte Carlo simulation
##################################################
counter_availability = np.zeros(len(time_axis)) # Initialize a counter for availability at each time step.

for i in range(stories):
    t = 0
    working = True

    while t < mission_time:
        if working:
            # Calculate the time index before the failure occurs
            t_pre = np.searchsorted(time_axis, t)
            # Generate a random failure time based on the failure rate
            t = t - np.log(1 - np.random.rand()) / failure_rate
            # Calculate the time index after the failure occurs
            t_post = np.searchsorted(time_axis, t)
            # Update the availability counter for the time interval between t_pre and t_post
            counter_availability[t_pre:t_post] += 1
            # Set the system to non-working state
            working = False
        else:
            # Generate a random repair time based on the repair rate
            t = t - np.log(1 - np.random.rand()) / repair_rate
            # Calculate the time index when the repair is completed
            repair_steps = np.searchsorted(time_axis, t)
            # Set the system to working state
            working = True

# Calculate the simulated system availability based on Monte Carlo trials.
availability_mc = counter_availability/stories 
# Calculate the theoretical true availability based on the specified failure and repair rates.
availability_true = (repair_rate) / (failure_rate + repair_rate) + (failure_rate / (failure_rate + repair_rate)) * np.exp(-(failure_rate + repair_rate) * time_axis)

##################################################
# Plot the results
##################################################
plt.figure()
plt.plot(time_axis, availability_true, label='True Availability')
plt.plot(time_axis, availability_mc, label='MC Availability')
plt.title("System Availability Over Time")
plt.legend()
plt.xlabel("Time (hours)")
plt.ylabel("Availability")
plt.show()