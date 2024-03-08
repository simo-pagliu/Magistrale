## CHERNOBYL - SIMPLE REACTOR MODEL
#the simple reactor model using the Reactor Time constant is userful to understand the dynamics of
#accidental scenarios, so let's try to compute how much power was released in the Chernobyl accident

## PARAMETERS
#
#from loss of control to explosion it took 4 seconds
t_interval = 4 #seconds

#nominal power of the reactor
P_nominal = 3200e6 #W

#it started at 20% of the nominal power, then rose up to 100x the nominal power
P_initial = 0.2*P_nominal #MW
P_final = 100*P_nominal #MW


## COMPUTING THE REACTOR TIME
#
#T = l/(k-1)
#but we can also invert the power law:
#P = P_initial*e^(delta_t/T) --> get T
#here, for the sake of readability, we will use symbolic vars
import sympy as sp #import the symbolic library
t_reactor = sp.symbols('t_reactor', positive=True, real=True) #define the variable and its conditions
eq = sp.Eq(P_initial*sp.exp(t_interval/t_reactor), P_final) #power law
t_reactor = sp.solve(eq, t_reactor) #solve to get the reactor time
t_reactor = float(t_reactor[0]) #you have to specify the index even if it returns just one value
print(f"The reactor time T = {t_reactor}s")

## COMPUTING THE ENERGY RELEASED
#
#the energy released is the integral of the power over time
t = sp.symbols('t', positive=True, real=True) #define the variable and its conditions
Power = sp.Function('Power')(t) #define the power as a function of time
Power = P_initial*sp.exp(t/t_reactor) #power law
Energy = sp.integrate(Power, (t, 0, t_interval)) #compute the integral between 0 and the time interval (4 seconds)
Energy = float(Energy) #convert to float
print(f"The energy released was {Energy:.2e}J") #print the result
Tons_TNT = round(Energy/4.184e9) #convert to tons of TNT: 4.184e+9 J = 1 ton of TNT
print(f"Which is equivalent to ~{Tons_TNT} tons of TNT") #print the result
