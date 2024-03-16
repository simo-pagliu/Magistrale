#Execrise presented and solved during the lesson of 21/02/2024 with analytical solution

#Evaluation of the quantity of a radionuclide in a loop where it gets activated only in a portion of the loop 
#(for instace inside the reactor core)
#and a second portion in which it only experiences deacy
#the script solves the differential equation by iteration, step by step, for each loop (fixed number of loops)
#the source term is "deactivated" every odd iteration (even iteration = in the core, odd iteration = outside the core)

import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

#initial conditions
y0 = 0 #initial condition
t_i = 0 #initial time

#constants
decay_const = 0.05 #decay constant
source = 0.75 #source term
t1 = 10 #first step time (when the source term is present)
t2 = 5 #second step time (when the source term is not present)

#for loop
for i in range(0, 10):

#final time of the step
    if i%2 == 0:
        t_f = t_i + t1 
    else:
        t_f = t_i + t2
    
#source term is present only in the first step of each loop
    if not i%2 == 0:
        src = 0
    else:
        src = source

    #define a linear differential equation where y is the dependent variable and t is the independent variable
    #dy/dt = -decay_const * y + src
    def model(y, t):
        dydt = -decay_const * y + src
        return dydt


    t = np.linspace(t_i, t_f, 100) #time points
    y = odeint(model, y0, t) #solve ODE

    y0 = y[-1] #new initial condition
    t_i = t_f #new initial time

    #i want to save the results of each loop
    if i == 0:
        y_tot = y
        t_tot = t
    else:
        y_tot = np.concatenate((y_tot, y))
        t_tot = np.concatenate((t_tot, t))


#plot results
plt.plot(t_tot, y_tot)
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()
