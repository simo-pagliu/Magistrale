#import numpy and plot
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

#Data given in the problem that does not change
Tau_Iodine = 6.57 #hours
lambda_Iodine = np.log(2)/(Tau_Iodine*3600)

Tau_Xenon = 9.14 #hours
lambda_Xenon = np.log(2)/(Tau_Xenon*3600) 

Yield_Iodine = 0.0639
Yield_Xenon = 0.00237

#Time 
t_i = 0
t_stop = 24*3600*2 #4 days, then scrammed
t_1 = np.linspace(t_i,t_stop,1000) #from startup to scram
t_scrammed = t_stop + 24*3600*2 #2 days off
t_2 = np.linspace(t_stop, t_scrammed, 1000) #from scram to criticality
t_f = t_scrammed + 24*3600*2 #10 days of criticality
t_3 = np.linspace(t_scrammed, t_f, 1000) #from scrammed to full power

#function to solve the system of differential equations
def solve_system(Rate_Fission, Rate_Capture, Iodine_0, Xenon_0, Cesium_0, t_interval):
    t = sp.symbols('t')
    Iodine = sp.Function('Iodine')(t)
    Xenon = sp.Function('Xenon')(t)
    Cesium = sp.Function('Cesium')(t)
    eq1 = sp.Eq(Iodine.diff(t), -lambda_Iodine*Iodine + Rate_Fission*Yield_Iodine) 
    eq2 = sp.Eq(Xenon.diff(t), -lambda_Xenon*Xenon - Rate_Capture*Xenon + Yield_Xenon*Rate_Fission + lambda_Iodine*Iodine)
    eq3 = sp.Eq(Cesium.diff(t), lambda_Xenon*Xenon)
    initial_conditions={Iodine.subs(t, 0): Iodine_0, Xenon.subs(t, 0): Xenon_0, Cesium.subs(t, 0): Cesium_0}
    sol = sp.dsolve((eq1, eq2, eq3), ics=initial_conditions)

    #Compute the values of the solution
    Iodine = sol[0].rhs
    Xenon = sol[1].rhs
    Cesium = sol[2].rhs

    #convert solutions to numpy functions
    Iodine = sp.lambdify(t, Iodine, 'numpy')
    Xenon = sp.lambdify(t, Xenon, 'numpy')
    Cesium = sp.lambdify(t, Cesium, 'numpy')

    #compute the solution in the time interval
    Iodine = Iodine(t_interval)
    Xenon = Xenon(t_interval)
    Cesium = Cesium(t_interval)

    return Iodine, Xenon, Cesium


## T_1: POWER IS ON

#set parameters and initial conditions
Rate_Fission = 9.34e19
Rate_Capture = 8.1e-5
Iodine_0 = 1
Xenon_0 = 0
Cesium_0 = 0

#solve the system
Iodine_t1, Xenon_t1, Cesium_t1 = solve_system(Rate_Fission, Rate_Capture, Iodine_0, Xenon_0, Cesium_0, t_1)


## T_2: SCRAM

#set parameters and initial conditions
Rate_Fission = 0
Rate_Capture = 0
Iodine_0 = Iodine_t1[-1]
Xenon_0 = Xenon_t1[-1]
Cesium_0 = Cesium_t1[-1]

#solve the system
Iodine_t2, Xenon_t2, Cesium_t2 = solve_system(Rate_Fission, Rate_Capture, Iodine_0, Xenon_0, Cesium_0, t_2)


## T_3: POWER IS BACK ON

#set parameters and initial conditions
Rate_Fission = 9.34e19
Rate_Capture = 8.1e-5
Iodine_0 = Iodine_t2[-1]
Xenon_0 = Xenon_t2[-1]
print(Xenon_0)
Cesium_0 = Cesium_t2[-1]

#solve the system
Iodine_t3, Xenon_t3, Cesium_t3 = solve_system(Rate_Fission, Rate_Capture, Iodine_0, Xenon_0, Cesium_0, t_3)


## Concatenation of the vectors

Iodine_vect = np.concatenate((Iodine_t1, Iodine_t2, Iodine_t3))
Xenon_vect = np.concatenate((Xenon_t1, Xenon_t2, Xenon_t3))
Cesium_vect = np.concatenate((Cesium_t1, Cesium_t2, Cesium_t3))
t_vect = np.concatenate((t_1, t_2, t_3))

## Plot
plt.plot(t_vect/3600, Iodine_vect, label='Iodine Concentration')
plt.plot(t_vect/3600, Xenon_vect, label='Xenon Concentration')
plt.plot(t_vect/3600, Cesium_vect, label='Cesium Concentration')
plt.legend()
plt.xlabel("time [h]")
plt.ylabel("Concentration normalized")
plt.yscale('log')
plt.grid()
plt.show()




