#Exercise presented during the lecture of 21/02/2024

#Consider the Xeon production in a reactor
#The Iodine135 is produced by fission, it then deacys into Xenon135, which can decay either beta, or absorb a neutron and become Xe136, which will then later on, undergo fission
#Determine the concentration of Iodine and Xeonon

#import modules to solve differential equations
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from scipy.interpolate import interp1d

#Constants
Tau_Iodine = 6.57 #hours
lambda_I = np.log(2)/(Tau_Iodine*3600)

Tau_Xenon = 9.14 #hours
lambda_Xe = np.log(2)/(Tau_Xenon*3600) 


src_Iodine = 5e-12  # Source term of Iodine135

Yield_Iodine = 0.0639
Yield_Xenon = 0.00237

Rate_Fission = 9.34e19
Rate_Capture = 8.1e-5

#initial conditions
y0_Iodine = 0 #initial condition for Iodine
y0_Xenon = 0 #initial condition for Xenon

#time point for the solutions
t_i = 0 #initial time
t_f = 3600*24*3 #final time
t_array = np.linspace(t_i, t_f, 480) #time points
t_array = np.array(t_array).flatten()
t_stop = 24*3600 #time at which the source term stops


#define differential equation for Iodine
def Iodine_Eq(y, t):

    if t>t_stop:
        src = 0
    else:
        src = 1

    # Differential equations
    dIodine_dt = -lambda_I * y + src*(Rate_Fission*Yield_Iodine - Rate_Capture*Yield_Xenon)

    return dIodine_dt



#solve the differential equation for Iodine
Iodine_Sol = odeint(Iodine_Eq, y0_Iodine, t_array) #solve ODE
#convert the solution to an array
Iodine_Sol = np.array(Iodine_Sol).flatten()

#interpolate the derivative of the solution of Iodine
#define a function for the derivative of the solution starting from dydt_Iodine
Iodine_Sol_Array = interp1d(t_array, Iodine_Sol, bounds_error=False, fill_value="extrapolate") #apparently this returns a function which is a different type of object
print(type(Iodine_Sol_Array))

#define differential equation for Xenon
def Xenon_Eq(y, t):
    
    if t>t_stop:
        src = 0
    else:
        src = 1

    # Differential equations
    dXenon_dt = -lambda_Xe * y + lambda_I * Iodine_Sol_Array(t)

    return dXenon_dt


#solve the differential equation for Xenon
Xenon_Sol = odeint(Xenon_Eq, y0_Xenon, t_array)
#convert the solution to an array
Xenon_Sol = np.array(Xenon_Sol).flatten()

#plot iodine and xenon solution on the same plot
plt.plot(t_array, Iodine_Sol, label="Iodine")
plt.plot(t_array, Xenon_Sol, label="Xenon")
#plt.plot(t_array, dydt_Iodine, label="dydt_Iodine")
#plt.plot(t_array, y_analytical, label="Analitic_Iodine")
plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend()
plt.show()



