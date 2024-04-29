#During lecture 4, she presented the python code starting from already computed analytical solution of the differential equations.
#here we present the code starting from the differential equations and solving them with sympy
#because this makes sense...for fuck sake

#import modules useful for solving differential equations, use laplace transform, and plot the results
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

## DEFINITION OF THE PROBLEM

#define constants
T_iodine = 6.57 #hours
T_xenon = 3.818 #hours

convertion = lambda tau: np.log(2)/(tau*3600) #convertion from hours to seconds and computatuiin of deacy constant

Lambda_Iodine = convertion(T_iodine) #decay constant for iodine
Lambda_Xenon = convertion(T_xenon) #decay constant for xenon

Iodine_0 = 1 #initial iodine concentration
Xenon_0 = 0 #initial xenon concentration
Cesium_0 = 0 #initial cesium concentration

## SYSTEM SOLUTION

#define a sistem of three differential first order equations
t = sp.symbols('t')
Iodine = sp.Function('Iodine')(t)
Xenon = sp.Function('Xenon')(t)
Cesium = sp.Function('Cesium')(t)
eq1 = sp.Eq(Iodine.diff(t), -Lambda_Iodine*Iodine)
eq2 = sp.Eq(Xenon.diff(t), -Lambda_Xenon*Xenon + Lambda_Iodine*Iodine)
eq3 = sp.Eq(Cesium.diff(t), Lambda_Xenon*Xenon)

#solve the sistem of differential equations with the initial conditions
initial_conditions={Iodine.subs(t, 0): Iodine_0, Xenon.subs(t, 0): Xenon_0, Cesium.subs(t, 0): Cesium_0}
sol = sp.dsolve((eq1, eq2, eq3), ics=initial_conditions)

#display the results
print(sol)

## LIMITS AT INFINITY

#compute the limit for t->inf
Iodine_inf = sp.limit(sol[0].rhs, t, sp.oo)
print(f"The limit for t->inf of Iodine is: {Iodine_inf}")

# for some reasons the limit for Xenon is not computed
# Xenon_inf = sp.limit(sol[1].rhs, t, sp.oo)
# print(f"The limit for t->inf of Xenon is: {Xenon_inf}")

#compute the limit for t->inf
Cesium_inf = sp.limit(sol[2].rhs, t, sp.oo)
print(f"The limit for t->inf of Cesium is: {Cesium_inf}")

#check when the limit is reached
#convert to lambda function to perform numeric evaluation
Cesium_lambda = sp.lambdify('t', sol[2].rhs, 'numpy')

t_eval = 0
while Cesium_lambda(t_eval) < Cesium_inf:
    t_eval += 1*3600 #add 1 hour
t_eval = t_eval/(24*3600) #convert to days
print(f"The limit for Cesium is reached after = {t_eval} days")

## COMPUTE THE DERIVATIVES
Iodine_rate = sp.diff(sol[0].rhs, t)
Xenon_rate = sp.diff(sol[1].rhs, t)
Cesium_rate = sp.diff(sol[2].rhs, t)

#lambda functions for the derivatives
Iodine_rate_lambda = sp.lambdify('t', Iodine_rate, 'numpy')
Xenon_rate_lambda = sp.lambdify('t', Xenon_rate, 'numpy')
Cesium_rate_lambda = sp.lambdify('t', Cesium_rate, 'numpy')

## PLOTTING

#time interval for plotting
t_i = 0
t_f = 3*24*3600 #3 days
t = np.linspace(t_i, t_f, 1000)

#convert symbolic solutions to numerical functions for plotting
Iodine = sp.lambdify('t', sol[0].rhs, 'numpy')
Xenon = sp.lambdify('t', sol[1].rhs, 'numpy')
Cesium = sp.lambdify('t', sol[2].rhs, 'numpy')

#plot the results
plt.plot(t, Iodine(t), label='Iodine')
plt.plot(t, Xenon(t), label='Xenon')
plt.plot(t, Cesium(t), label='Cesium')
plt.xlabel('Time (seconds)')
plt.ylabel('Concentration')
plt.title('Concentration of isotopes')
plt.legend()
plt.show()

#plot the derivatives
plt.plot(t, Iodine_rate_lambda(t), label='Iodine rate')
plt.plot(t, Xenon_rate_lambda(t), label='Xenon rate')
plt.plot(t, Cesium_rate_lambda(t), label='Cesium rate')
plt.xlabel('Time (seconds)')
plt.ylabel('Rate')
plt.title('Rate of isotopes')
plt.legend()
plt.show()


