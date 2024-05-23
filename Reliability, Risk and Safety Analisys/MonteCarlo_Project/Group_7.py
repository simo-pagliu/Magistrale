##################################################
# MONTECARLO PROJECT - Assignment H (a.y.: 2023-24)
# Reliability, Risk and Safety Analysis
#
# Group 7
#
# Members:
# - Pagliuca Simone  
# - Mezzaro Samuele
# - Cyrille de Lurions
#
# Check "USER CONFIG" and "GLOBAL VALUES" sections
# before running the code.
#
# To run the second request, set COMMON_RATE = 1.5e-3 (in the GLOBAL VALUES section)
# To run the first request, set COMMON_RATE = 0 (in the GLOBAL VALUES section)
#
##################################################

##################################################
# IMPORTS NEEDED PACKAGES
##################################################
import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt

##################################################
# USER CONFING
##################################################
DEBUG = False # Set to True to enable debug prints, waits for input after each step
SOLVE_ANALYTICAL = False # Set to True to solve the analytical solution and have it plotted

##################################################
# GLOBAL VALUES
##################################################
REPAIR_RATE = 2.2e-1
FAIL_RATE = 5.5e-3
COMMON_RATE = 1.5e-3 # Set this value to 0 to solve the first request, otherwise set it to 1.5e-3
COMMON_PROB = 0.4
STORIES = 10000 # Number of Monte Carlo trials to simulate
MISSION_TIME = 1000 # Mission time in hours
TIME_AXIS = np.linspace(0, MISSION_TIME, 1000) # Create a time axis from 0 to mission_time.

##################################################
# COMPUTES ANALYTICAL SOLUTION
##################################################
def analytical():
    global FAIL_RATE, REPAIR_RATE, TIME_AXIS, COMMON_RATE, COMMON_PROB
    print("\033[91m {}\033[00m" .format("You set SOLVE_ANALYTICAL=TRUE, Computing Analytical Solution, This might take a while..."))
    
    ### Availability ###

    # Define the time variable
    t = sp.symbols('t', positive=True, real=True)

    # Define the functions
    x = sp.Function('x1', positive=True)(t)
    y = sp.Function('x2', positive=True)(t)
    z = sp.Function('x3', positive=True)(t)
    w = sp.Function('x4', positive=True)(t)

    # Define the matrix of the system 4x4
    A = sp.Matrix([[-4*FAIL_RATE, 0, REPAIR_RATE, 0],
                [4*FAIL_RATE, -6*FAIL_RATE, 0, REPAIR_RATE],
                [0, 6*FAIL_RATE, -8*FAIL_RATE - REPAIR_RATE, 0],
                [0, 0, 8*FAIL_RATE, -REPAIR_RATE]])

    # Define the vector of the system 4x1
    X = sp.Matrix([x, y, z, w])

    # Define the right-hand side of the system
    B = sp.Matrix([sp.diff(x), sp.diff(y), sp.diff(z), sp.diff(w)])

    # Define the system of differential equations
    eqs = A*X - B

    # Solve the system of differential equations, with initial conditions x=1, y=0, z=0, w=0
    solution = sp.dsolve(eqs, ics={x.subs(t, 0): 1, y.subs(t, 0): 0, z.subs(t, 0): 0, w.subs(t, 0): 0})

    # Extract q1, q2, q3, q4 from the solution
    q1 = solution[0].rhs
    q2 = solution[1].rhs
    q3 = solution[2].rhs

    # Sum up only success states
    availability = q1 + q2 + q3
    Avail_Values = np.array([availability.subs(t, value).evalf() for value in TIME_AXIS])

    ### Reliability ###

    # Define the time variable
    t = sp.symbols('t', positive=True, real=True)

    # Define the functions
    x = sp.Function('x1', positive=True)(t)
    y = sp.Function('x2', positive=True)(t)
    z = sp.Function('x3', positive=True)(t)
    w = sp.Function('x4', positive=True)(t)

    # Now solve them again but remove the last column and last row of the matrix A
    A = sp.Matrix([[-4*FAIL_RATE, 0, REPAIR_RATE],
                    [4*FAIL_RATE, -6*FAIL_RATE, 0],
                    [0, 6*FAIL_RATE, -8*FAIL_RATE - REPAIR_RATE]])
    B = sp.Matrix([sp.diff(x), sp.diff(y), sp.diff(z)])
    X = sp.Matrix([x, y, z])
    eqs = A*X - B
    solution = sp.dsolve(eqs, ics={x.subs(t, 0): 1, y.subs(t, 0): 0, z.subs(t, 0): 0})

    # Extract r1, r2, r3 from the solution
    r1 = sp.re(solution[0].rhs)
    r2 = sp.re(solution[1].rhs)
    r3 = sp.re(solution[2].rhs)

    # Sum up
    reliability = r1 + r2 + r3
    Rely_Values = np.array([reliability.subs(t, value).evalf() for value in TIME_AXIS])
  

    return Avail_Values, Rely_Values

##################################################
# COMPUTES THE TRANSITION MATRIX
##################################################
def trans_matrix(system):
    global REPAIR_RATE, FAIL_RATE, COMMON_RATE

    num_working_components = np.sum(system)

    repair = REPAIR_RATE if num_working_components <= 2 else 0
    fail = num_working_components*((2**(4-num_working_components)) * FAIL_RATE) if num_working_components > 1 else 0

    # Define the transition matrix [F, W, CF*] x [F, W, CF]     (* = Omissis because [0 0 0])
    Transition_Matrix = np.array([[0, repair, 0],
                  [fail, 0, COMMON_RATE]])
    if DEBUG:
        print("Transition Matrix \n", Transition_Matrix)
        print("\n")
    return Transition_Matrix

##################################################
# COMPUTES COMMON FAILURE PROBABILITIES
##################################################
def common_fail(system):
    global COMMON_PROB
    # Generates a vector of all possible probabilities of faliure 
    common_trans_probs = []
    for ii in np.arange(sum(system)): # Takes all working components
        num_fails = 1 + ii # Plus one, to get the number of components that can fail
        # print("Number of components failing due to common failures", num_fails)

        tot = len(system) # Total number of components

        # Probability of faliure given by the binomial distribution
        prob = math.comb(tot, num_fails) * (COMMON_PROB**num_fails) * ((1-COMMON_PROB)**(tot - num_fails))
        common_trans_probs.append(prob) # Add the value to the vector
    # print("Common transition probabilities",common_trans_probs)
        

    # Calculate the cumulative distribution of the failure probabilities
    common_distribution = np.cumsum(common_trans_probs / np.sum(common_trans_probs))
    # print("Common transition rates", common_distribution)  
    # Generate a random number
    rand = np.random.rand()  
    # print("Random Number for the choiche of common transition ",rand)      
    # Find how many component that fails by comparing the random number to the distribution
    Num_Common_Fails = np.where(rand <= common_distribution)[0][0] + 1 # Plus one, to get the number of components that can fail
    
    if DEBUG:
        print("Failure Distribution", common_distribution)
        print("Random Number for the choiche of common transition ",rand)
        print("Failed components due to common failures", Num_Common_Fails)
        print("Common transition probabilities",common_trans_probs)
        print("\n")
    return Num_Common_Fails

##################################################
# SAMPLING THE COMPONENT
##################################################
def component_sample(TRANS, system):
    # Calculate the transition rates for each component
    Sys_Rates = [np.sum(TRANS[i]) for i in system]
    # print("Rates for each component", Sys_Rates)    
    # Calculate the cumulative distribution of the rates
    component_distribution = np.cumsum(Sys_Rates / np.sum(Sys_Rates))
    # print("Component Distribution", component_distribution)
    # Generate a random number
    rand = np.random.rand()
    # print("Random Number for the choiche of component ",rand)
    # Find the component that fails by comparing the random number to the distribution
    Component = np.where(rand <= component_distribution)[0][0]
    # print("Component that is transitioning: ", Component)

    if DEBUG:
        print("Rates for each component", Sys_Rates) 
        print("Component Distribution", component_distribution)
        print("Random Number for the choiche of component ",rand)
        print("Component that is transitioning: ", Component)
        print("\n")
    return Sys_Rates, Component

##################################################
# SAMPLING THE TRANSITION
##################################################
def transition_sample(trans, system, component):
    # Extract the transition rates for the chosen component
    transition_rates_chosen_component = trans[system[component]]
    # print("Chosen Transition", transition_rates_chosen_component)
    # Normalize the transition rates
    rates = transition_rates_chosen_component / np.sum(transition_rates_chosen_component)
    # print("Rates for each transition", rates)
    # Calculate the cumulative distribution of the rates
    transition_distribution = np.cumsum(rates)
    # print("Transition Distribution", transition_distribution)
    # Generate a random number
    rand = np.random.rand()
    # print("Random Number for the choiche of transition ",rand)
    # Find the transition that occurs by comparing the random number to the distribution
    Transition = np.where(rand <= transition_distribution)[0][0]
    # print("Transition", Transition)
    # Extract the transition rate
    # Just for debug purposes
    # transition_rate = transition_rates_chosen_component[Transition]
    # print("Transition Rate", transition_rate)

    if DEBUG:
        print("Chosen Transition", transition_rates_chosen_component)
        print("Rates for each transition", rates)
        print("Transition Distribution", transition_distribution)
        print("Random Number for the choiche of transition ",rand)
        print("Transition", Transition)
        transition_rate = transition_rates_chosen_component[Transition]
        print("Transition Rate", transition_rate)
        print("\n")

    return Transition

##################################################
# UPDATE TIME
##################################################
def update_time(time, sys_rates, component):
    global TIME_AXIS
    # print("Started at time ", time)
    sys_rate = sys_rates[component] # Get the system rate
    t_sample = - np.log(1 - np.random.rand()) / sys_rate # Compute the time interval
    New_Time = time + t_sample
    # print("Finished at time ", New_Time)
    Index_Pre = np.searchsorted(TIME_AXIS, time, side='left')
    Index_Post = np.searchsorted(TIME_AXIS, New_Time, side='left')
    # print("Index pre", Index_Pre, "Index post", Index_Post)

    if DEBUG:
        print("Started at time ", time)
        print("Finished at time ", New_Time)
        print("Index pre", Index_Pre, "Index post", Index_Post)
        print("\n")

    return New_Time, Index_Pre, Index_Post

##################################################
# UPDATE THE SYSTEM
##################################################
def update_system(System, component, transition):
    global COMMON_PROB
    Num_Common_Fails = 0 # Initialize the number of common failures since i can't return nothing

    if transition == 1:
        if DEBUG:
            print("\033[93mREPAIR\033[0m")
            print("Pre: ", System)
        # The repair process repairs 2 components at the same time
        System[component] = 1 # Repair the component that was sampled
        System[np.random.choice(np.where(System == 0)[0], 1)] = 1 # Repair another random component
        if DEBUG:
            print("Post:", System)

    elif transition == 0:
        if DEBUG:
            print("\033[93mFAILURE\033[0m")
            print("Pre: ", System)
        # The failure process fails 1 component
        System[component] = 0 # Fail the component that was sampled
        if DEBUG:
            print("Post:", System)
    
    elif transition == 2:
        if DEBUG:
            print("\033[93mCOMMON FAILURE\033[0m")
            print("Pre: ", System)
        # The common failure may fail 1 or all components
        Num_Common_Fails = common_fail(System)
        System[component] = 0 # Fail the component that was sampled
        other_faliures = Num_Common_Fails-1 # The common failure event can fail up to all working components
        if DEBUG:
            print("Number of other failures ", other_faliures)
        if other_faliures > 0:
            random_indexes = np.random.choice(np.where(System == 1)[0], other_faliures) # Choose N-1 random components
            System[random_indexes] = 0 # Fail N-1 random components
        if DEBUG:
            print("Post:", System)
    else:
        print("\033[91mThis Should Not Happend...\033[0m")
    if DEBUG:
        print("\n")

    return System , Num_Common_Fails

##################################################
# SIMULATE THE SYSTEM
##################################################
def simulate(system, time):
    global FAIL_RATE, REPAIR_RATE, COMMON_RATE, COMMON_PROB, TIME_AXIS, MISSION_TIME
    # First of all we reset some values
    first_failure = True
    Availability = np.zeros(len(TIME_AXIS))
    Reliability = np.ones(len(TIME_AXIS))
    TTF_Index = 0
    Num_Common_Fails = 0
    Num_Fails = 0
    Num_Repairs = 0 # We take into account the number of repairs, not the number of components repaired

    while time<MISSION_TIME:
        # Define the transition matrix
        matrix = trans_matrix(system)

        # Sample the component that will transition
        sys_rates, component = component_sample(matrix, system)

        # Sample the transition that will occur
        Transistion = transition_sample(matrix, system, component)

        # Update the time
        time, index_pre, index_post = update_time(time, sys_rates, component)

        # Update the system
        system, common_failed_comp = update_system(system, component, Transistion)

        ##################################################
        # UPDATE COUNTERS - A, R, TTF
        ##################################################
        if Transistion == 1 and sum(system)<4: # Repair && The repaired system has 3 or 2 working components, which means that it was in a 0/4 or 1/4 state before the repair, in those states the system is UNAVAILABLE
            Availability[index_pre:index_post] = 0 # Up until the moment it was repaired, it was not working
            if DEBUG:
                print(f"Availiability updated to 0 from {index_pre} to {index_post}")
            if first_failure == True: # If the flag is still True, it means that the system had not failed before
                Reliability[index_pre:] = 0 # From the moment it failed (time at which the repair started), it was not working anymore, note that reliability is defined as a vector of ones so i update the zeros
                first_failure = False # Set the flag to False, so that this block of code is not executed again
                TTF_Index = index_pre # Set the time to failure to the time at which the repair started
                if DEBUG:
                    print(f"Reliability updated to 0 from {index_pre} to the end of the mission, the failure occurred at index {index_pre}")
        else:
            Availability[index_pre:index_post] = 1 # Up until the moment it failed, it was working OR some components were repaired while the system was working
            if DEBUG:
                print(f"Availiability updated to 1 from {index_pre} to {index_post}")

        ##################################################
        # UPDATE LOG COUNTERS
        ##################################################
        if Transistion == 1:
            Num_Repairs += 1
            if DEBUG:
                print("Repair Interventions +1")
        elif Transistion == 0:
            Num_Fails += 1
            if DEBUG:
                print("Component Failed +1")
        else:
            Num_Common_Fails += common_failed_comp
            if DEBUG:
                print("Common Failure Event, added ", common_failed_comp, " components to the failed ones")
        
        ### DEBUGGING ###
        if DEBUG:
            input("Press Enter to continue...")
    ### END OF WHILE LOOP ###
        
    return Availability , Reliability, TTF_Index, Num_Common_Fails, Num_Fails, Num_Repairs

##################################################
# PLOT THE RESULTS
##################################################
def plot(availability_vect, reliability_vect):
    if SOLVE_ANALYTICAL:
        Avail_Values, Rely_Values = analytical()
    # Availability
    Availability_Values = availability_vect / STORIES
    Availability_Error = np.sqrt((abs(Availability_Values - Availability_Values**2)) / STORIES)
    plt.figure(1)
    plt.errorbar(TIME_AXIS, Availability_Values, yerr=Availability_Error, label='Montecarlo', linewidth=0.5)
    if SOLVE_ANALYTICAL:
        plt.plot(TIME_AXIS, Avail_Values, label='Analytical (First Request)', linestyle='--', linewidth=1.25)
    plt.title("System Availability Over Time")
    plt.legend()
    plt.xlabel("Time [hours]")
    plt.grid()

    # Reliability
    Reliability_Values = reliability_vect / STORIES
    Reliability_Error = np.sqrt((abs(Reliability_Values - Reliability_Values**2)) / STORIES)
    plt.figure(2)
    plt.errorbar(TIME_AXIS, Reliability_Values, yerr=Reliability_Error, label='Monecarlo', linewidth=0.5)
    if SOLVE_ANALYTICAL:
        plt.plot(TIME_AXIS, Rely_Values, label='Analytical (First Request)', linestyle='--', linewidth=1.25)
    plt.title("System Reliability Over Time")
    plt.legend()
    plt.xlabel("Time [hours]")
    plt.grid()

    # Show both figures
    plt.show()

##################################################
# MAIN
##################################################
def main():
    # Initize counters
    availability_vect = np.zeros(len(TIME_AXIS))
    reliability_vect = np.zeros(len(TIME_AXIS))
    ttf_indexes_vect = []

    # Initize log counters
    ii_repairs = np.zeros(STORIES)
    ii_fails = np.zeros(STORIES)
    ii_common = np.zeros(STORIES)

    print(f"\033[93mStarting Monte Carlo Simulation, {STORIES} Stories\033[0m")
    print("\n")

    # Simulation loop
    for ii in range(STORIES):
        # Reset values for the new story
        time = 0 
        system = np.array([1, 1, 1, 1]) # Initial state of the system, 1 = working, 0 = failed

        # Simulate the story
        availability , reliability, ttf_index, num_common_fails, num_fails, num_repairs = simulate(system, time)

        # Update global counters
        availability_vect += availability
        reliability_vect += reliability
        ttf_indexes_vect.append(ttf_index)

        # Update log counters
        ii_repairs[ii] = num_repairs
        ii_fails[ii] = num_fails
        ii_common[ii] = num_common_fails

        # Print progress and some logs
        if DEBUG:
            print("Story Finished\n")
            print(f"\033[93m Components Failed:{sum(ii_fails)} Components Repaired:{sum(ii_repairs)*2} Components Failed due to Common Failure Events:{sum(ii_common)} Progress:{(ii+1)}/{STORIES}\033[0m")
        else:
            print(f"\r\033[93m Components Failed:{sum(ii_fails)} Components Repaired:{sum(ii_repairs*2)} Components Failed due to Common Failure Events:{sum(ii_common)} Progress:{round(((ii+1)/STORIES) * 100,0)}%\033[0m", end="")
        
    ### END OF FOR LOOP ###

    print("\n")
    print("\033[92mMonte Carlo Simulation Completed\033[0m")

    with open('output.txt', 'w') as f:
        f.write(f"Monte Carlo Simulation Performed with {STORIES} Stories\n")
        # Number of maintenance interventions
        ii_repairs_error = np.std(ii_repairs) / np.sqrt(STORIES)
        ii_repairs = np.mean(ii_repairs)
        output = f"Number of maintenance interventions: {ii_repairs:.4f} ± {ii_repairs_error:.4f}"
        print(output)
        f.write(output + "\n")
    
        # Number of failed components
        tot_fails = np.mean(ii_fails + ii_common)
        tot_fails_err = np.std(ii_fails + ii_common) / np.sqrt(STORIES)
        output = f"Number of failed components: {tot_fails:.4f} ± {tot_fails_err:.4f}"
        print(output)
        f.write(output + "\n")
    
        # MTTF: Mean Time To Failure
        ttfs = TIME_AXIS[ttf_indexes_vect]
        MTTF_value = np.mean(ttfs)
        MTTF_error = np.std(ttfs)/np.sqrt(STORIES)
        output = f"Mean Time to failure {MTTF_value:.4f} ± {MTTF_error:.4f} hours"
        print(output)
        f.write(output + "\n")
    
    # Plot the results
    plot(availability_vect, reliability_vect)

if __name__ == "__main__":
    main()