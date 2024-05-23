import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Define the failure rate, the maintenance duration, and the time interval
Lambda = 3.5e-4
tau_m = 10
T_mission = 1000

STORIES = 1000
TIME_AXIS = np.linspace(0, T_mission+tau_m, 100000)
counter_avail = np.zeros(len(TIME_AXIS))
counter_rely = np.zeros(len(TIME_AXIS))
ttf_vect = np.zeros(STORIES)


for jj in range(STORIES):

    # Reset the system
    current_state = [1, 1] # A=working, B=working
    time = 0
    first_failure = True

    # Probability to start this cycle with a B failed
    prob = 1 - np.exp(-Lambda*(T_mission/2))
    if np.random.rand() < prob:
        current_state[1] = 0

    # By deault, the system is working
    counter_avail += 1

    # print(f"\r{ii}", end='')
    print(f"Starting state: {current_state}")

    # Simulate the system
    for ii in [1,2]: #2 half cycles
        print("Cycle: ", ii)
        while time < ii * T_mission/2:
            # This simulates the first half of the mission

            # Save the previous time
            time_prev = time

            # Sample the time to failure
            time_to_failure = - np.log(1 - np.random.rand()) / (sum(current_state)*Lambda) # Compute the time interval
            time += time_to_failure

            # If it was only one component working
            if sum(current_state) == 1:
                # That one failed
                current_state = [0, 0]
                # And from now on
                # The system will be broken until the end of the maintenance
                counter_avail[np.searchsorted(TIME_AXIS,time_prev,'left'):np.searchsorted(TIME_AXIS,ii*T_mission/2 + tau_m,'left')] -= 1 # During repair it wasn't working
                time = ii*T_mission/2 + tau_m # Jump to the end of the maintenance
                print(f"System failed at: {time}")
                if first_failure:
                    first_failure = False
                    counter_rely[np.searchsorted(TIME_AXIS,time,'left'):] += 1 # Before this first failure, the system was working
                    ttf_vect[jj] = time
                    print(f"First failure at: {time}")
            else:
                # Otherwise, choose one component to fail
                print("Choosing a component to fail")
                random_number = np.random.randint(0, 1)
                current_state[random_number] = 0


        # We get here only if the system didn't fail during the first half of the mission
        while time < ii*T_mission/2 + tau_m:
            print("Maintenance")
            # This simulates the maintenance
            # Save the previous time
            time_prev = time

            print(f"Now the component {ii-1} is under maintenance")
            current_state[ii-1] = 0 # A = under maintenance , B = working

            # If B is still working
            if sum(current_state) > 0:
                print("The other component is still working")
            # Sample the time to failure
                time_to_failure = - np.log(1 - np.random.rand()) / (sum(current_state)*Lambda) # Compute the time interval
                time += time_to_failure
            # If we sampled a time over the maintenance duration
            # Nothing will happen during the maintenance, so we jump to the end of it
            # Otherwise, the system will fail
                if time < T_mission/2 + tau_m:
                    print(f"System failed at during maintainance: {time}")
                    # Failing A
                    current_state[0] = 0
                    # The system will be broken until the end of the maintenance
                    counter_avail[np.searchsorted(TIME_AXIS,time,'left'):np.searchsorted(TIME_AXIS,ii*T_mission/2 + tau_m,'left')] -= 1 # During repair it wasn't working
                    if first_failure:
                        print(f"First failure during maintanace at: {time}")
                        first_failure = False
                        counter_rely[np.searchsorted(TIME_AXIS,time,'left'):] += 1 # Before this first failure, the system was working
                        ttf_vect[jj] = time
            # Otherwise, the system will fail
            else:
                print(f"System failed at during maintainance because the other component was already failed at time: {time}")
                counter_avail[np.searchsorted(TIME_AXIS,ii*T_mission/2,'left'):np.searchsorted(TIME_AXIS,ii*T_mission/2 + tau_m,'left')] -= 1 # During repair it wasn't working
                time = ii*T_mission/2 + tau_m # Jump to the end of the maintenance

        # Now B is repaired, A might be up or down
        current_state[ii-1] = 1


# Compute the MTTF
MTTF_val = np.sum(ttf_vect)/STORIES
MTTF_err = np.std(ttf_vect)/np.sqrt(STORIES)
print(f"\nMTTF: {MTTF_val} +- {MTTF_err}")

# Plot the availability
plt.figure(1)
avail = counter_avail/STORIES
err_avail = np.sqrt((avail - avail**2)/STORIES)
plt.plot(TIME_AXIS, avail)
# plt.errorbar(TIME_AXIS, avail, yerr=err_avail)
plt.xlabel('Time')
plt.ylabel('Availability')
plt.title('System Availability')

# Average availability
err_avg_avail = np.sqrt((np.mean(avail) - np.mean(avail)**2)/STORIES)
print(f"Average availability: {np.mean(avail)} +- {err_avg_avail}")

plt.figure(2)
rely = 1 - counter_rely/STORIES
err_rely = np.sqrt((rely - rely**2)/STORIES)
plt.errorbar(TIME_AXIS, rely, yerr=err_rely)
plt.xlabel('Time')
plt.ylabel('Reliability')
plt.grid()
plt.title('System Reliability')

plt.show()
