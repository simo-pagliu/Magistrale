import numpy as np
import matplotlib.pyplot as plt

# System parameters
lambda_f = 3.5e-4  # Failure rate [h^-1]
T = 1000  # Time interval between the end of the previous maintenance and the beginning of the next maintenance [h]
tau_m = 10  # Duration of maintenance intervention [h]
mu = 1/tau_m  # Repair rate [h^-1]
Tp = T + tau_m  # Total period of the maintenance cycle [h]

n_time = 1000 # Number of time steps
time_axis = np.linspace(0, Tp, n_time)  # Time axis [h]

# Analytical solution
av_an = lambda tt: np.exp(-lambda_f * tt)**2 
Time_axis = np.linspace(0, Tp, 1000)
Av_an = av_an(Time_axis)
Av_an[np.searchsorted(Time_axis, T) : ] = 0

# Monte Carlo simulation
N = 10000 # Number of Monte Carlo trials
q_counter = np.zeros(len(time_axis))

for _ in range(N):
    sys_flag = True  # Reset system state for each simulation
    t = 0
    
    while t < Tp:  # Simulate until the end of maintenance cycle
        if sys_flag:
            t_1 = t + np.random.exponential(1/lambda_f)  # Time of the first failure
            t_2 = t + np.random.exponential(1/lambda_f)  # Time of the second failure
            t = max(t_1, t_2)  # Update the current time to the maximum of the two failure times
            sys_flag = False
            # Update the counter from t to T
            t_min = min(t_1, t_2)  # Minimum failure time
            q_counter[np.searchsorted(time_axis, t_min):np.searchsorted(time_axis, T)] += 1  # Increment the counter for the corresponding time range
        else:
            q_counter[np.searchsorted(time_axis, T):] += 1  # Increment the counter for the remaining time range
            t = Tp  # Set the current time to the end of the maintenance cycle
            


# Calculate the time dependant availability from the Monte Carlo simulation and adjust it to from T to Tp
Av_mc = 1 - q_counter / N
Av_mc[np.searchsorted(time_axis, T):] = 0

# Calculate the time dependant uncertainty of the Monte Carlo solution
Unc_MC = np.zeros(len(Av_mc))
for i in range(len(Av_mc)):
    Unc_MC[i] = np.std(Av_mc[i:])


# Calculate mean and standard deviation of availability from the Monte Carlo simulation and print them
mean_av = np.mean(Av_mc)
std_av_mc = np.std(Av_mc)
print('Monte Carlo mean availability: ', mean_av)
print('Monte Carlo standard deviation of availability:', std_av_mc)

# Calculate mean and standard deviation of availability from the analytical solution and print them
mean_av_an = np.trapz(Av_an, time_axis) / Tp
std_av_an = np.std(Av_an)
print('Analytical mean availability:', mean_av_an)
print('Analytical standard deviation of availability:', std_av_an)

# Plot the Monte Carlo and analytical solutions over one complete cycle
plt.figure(1)
plt.plot(time_axis, Av_mc, label='Monte Carlo simulation')
plt.plot(time_axis, Av_an, label='Analytical solution', linestyle='--')
plt.xlabel('Time [h]')
plt.ylabel('Availability')
plt.title('Monte Carlo availability')
plt.legend()
plt.grid()
plt.show()

# Plot the uncertainty of the Monte Carlo solution over one complete cycle
plt.figure(2)
plt.plot(time_axis, Unc_MC)
plt.xlabel('Time [h]')
plt.ylabel('σ_A(t)')
plt.title('Uncertainty of Monte Carlo availability')
plt.grid()
plt.show()