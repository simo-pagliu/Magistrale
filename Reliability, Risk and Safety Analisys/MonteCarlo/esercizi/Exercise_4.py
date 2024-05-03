import numpy as np
import matplotlib.pyplot as plt

# System parameters for components A, B, and C
lambda_A, mu_A = 1e-3, 3e-2
lambda_B, mu_B = 2e-2, 5e-2
lambda_C, mu_C = 5e-2, 5e-3

# Transition matrices for components A, B, and C
Trans_A = np.array([[0, lambda_A], [mu_A, 0]])
Trans_B = np.array([[0, lambda_B], [mu_B, 0]])
Trans_C = np.array([[0, lambda_C], [mu_C, 0]])

# Failed system states (cut sets) adjusted for 0 as working and 1 as failed
failed_states = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 1]])

# Initial system state (all components operational)
initial_state = np.array([0, 0, 0])


# Simulation parameters
Tm = 500  # Mission time
N = 100000  # Number of Monte Carlo trials
Dt = 1  # Time step
Time_axis = np.arange(0, Tm + Dt, Dt)

# Initialize counters for unreliability and unavailability
unrel = np.zeros(len(Time_axis))
counter_q = np.zeros(len(Time_axis))

# initialize the lambda of each component
lambda_out=np.zeros(len(initial_state))

# Main Monte Carlo cycle
for n in range(N):
    first_failure_flag = False
    t = 0
    failure_flag = False
    current_state = initial_state.copy()
    prev_system_state_flag = 0  # Adjusted to 0 for working state
    
    # Simulation loop
    while t < Tm:
        # Calculate the transition rate for each component
        lambda_out[0]=np.sum(Trans_A[current_state[0], :])
        lambda_out[1]=np.sum(Trans_B[current_state[1], :])
        lambda_out[2]=np.sum(Trans_C[current_state[2], :])
        # Calculate the transition rate of the system
        lambda_sys = np.sum(lambda_out)

        # Sample transition time (t_trans)
        t_trans = -1 / lambda_sys * np.log(np.random.rand())
        t += t_trans

        # You are asked to:
            #1) sample which type of transition has occurred, i.e. which component 
            #has undergone the transition and to which arrival state.
            #2) keep going up to the mision time (Tm) by computing the time dependent
            #Reliability and the instantaneous Availability

# Estimate reliability and availability from Monte Carlo samples
Mean_rel = 1 - unrel / N
sig_rel = np.sqrt((Mean_rel - Mean_rel**2) / N)
Av_MC = 1 - counter_q / N
sig_av = np.sqrt((Av_MC - Av_MC**2) / N)

# Analytical reliability function (lambda is used to define an anonymous function)
rel_an = lambda tt: np.exp(-lambda_A * tt) + np.exp(-(lambda_B + lambda_C) * tt) - np.exp(-(lambda_A + lambda_B + lambda_C) * tt)

# Plotting results
plt.figure(1)
plt.plot(Time_axis, Mean_rel, label='MC estimation')
plt.plot(Time_axis, rel_an(Time_axis), label='Analytical reliability')
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('R(t)')
plt.legend()

plt.figure(2)
plt.plot(Time_axis, sig_rel)
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('σ_R(t)')

plt.figure(3)
plt.plot(Time_axis, Av_MC)
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('Av(t)')

plt.figure(4)
plt.plot(Time_axis, sig_av)
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('σ_A(t)')

plt.show()
