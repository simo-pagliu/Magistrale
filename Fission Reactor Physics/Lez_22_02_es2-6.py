import sympy
import numpy as np

x = sympy.symbols('x')

#constants
a = 1
b = 104 #tot cross-section [1/cm]

#define an exponential function with the symbolic vaiable x
attenuation_law = a * sympy.exp(-b*x)

#set the desired objective
objective = 0.001

#solve the equation for x
solution = sympy.solve(attenuation_law - objective, x)
#take only the real solutions
#solution = [i.evalf() for i in solution if i.is_real]

for i in solution:
    if i.is_real:
        solution = i.evalf()
print(str(solution) + " cm")

#plot the function
sympy.plot(attenuation_law, (x, 0, 10), ylabel='attenuation(x)')


