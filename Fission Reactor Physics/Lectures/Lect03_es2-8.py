#exercise 2.8 "due to home" last slide on Lecture 3
 
#import packages
import math
import sympy

t_1 = 5*60 #first time stamp
t_2 = 7*60 #second time stamp

t = sympy.symbols('t')

#define constants
half_life = 11.1 #min
tot_cross_sec = 3.45
vel = 2200

#deacy constant
decay_const = math.log(2) / (half_life*60)

#probability of no decay in time t_1
no_decay = math.exp(-decay_const*t_1)
#probability of no interaction in time t
no_interaction = sympy.exp(-tot_cross_sec*1e-2*vel*t_1)

#tot probability during t_1
prob_t1 = no_decay*no_interaction

#probability to have deacy in time t;t+dt
decay = prob_t1*(decay_const*t)
#probability to have interaction in time t;t+dt
interaction = prob_t1*(tot_cross_sec*1e-2*vel*t)

#integrate deacy over time
decay_int = sympy.integrate(decay, (t, t_1, t_2))
#integrate interaction over time
interaction_int = sympy.integrate(interaction, (t, t_1, t_2))

#print the ration between the two results
print(f"Ratio between the two: {decay_int/interaction_int:.2e}")

#technically...
teo = decay_const/(tot_cross_sec*1e-2*vel)
print(f"The ratio from the analitical solution got by hand (see notes):  {teo}")


