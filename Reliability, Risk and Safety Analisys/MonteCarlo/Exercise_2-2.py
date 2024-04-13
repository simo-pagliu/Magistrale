import numpy as np
import matplotlib.pyplot as plt

# Initialize simulation parameters
Mission_Time = 1000  # Mission time in hours
stories = 10000  # Number of Monte Carlo trials
fail_rate = 3e-3  # Failure rate
t_interval = 1  # Bin length in hours for time axis
Time_axis = np.arange(0, Mission_Time + t_interval, t_interval)  # Time axis from 0 to Tm with step size Dt

# Initialize a counter for failures at each time step
counter_fails = np.zeros(len(Time_axis))

# Monte Carlo simulation to estimate reliability
for i in range(stories):
    #Simulate the component failure time and increase by 1 all the counters in "counter_f" associated to times successive to the failure occurence time

    # Generate a random failure time based on the failure rate
    t_fail = -np.log(1 - np.random.rand()) / fail_rate
    # Calculate the time index when the failure occurs
    fail_steps = np.searchsorted(Time_axis, t_fail)
    # Update the failure counter for the time interval after the failure occurs
    counter_fails[fail_steps:] += 1


# Calculate reliability based on Monte Carlo simulation
Rel_MC = 1 - counter_fails / stories
# Calculate true reliability using analytical expression
Rel_true = np.exp(-fail_rate * Time_axis)

# Plotting the results
plt.figure()
plt.plot(Time_axis, Rel_true, 'blue', label='True Reliability')  # Plot true reliability curve
plt.plot(Time_axis, Rel_MC, 'red', label='MC Simulated Reliability')  # Plot Monte Carlo estimated reliability curve

# Add plot details
plt.title("Reliability Comparison")
plt.legend()
plt.xlabel("Time [h]")
plt.ylabel("Reliability, R(t)")
plt.show()
