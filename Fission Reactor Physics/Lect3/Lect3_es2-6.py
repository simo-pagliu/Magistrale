#exercise 2.6 "due to home" last slide on Lecture 3

#import modules
import sympy

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

for ii in solution:
    if ii.is_real:
        solution = ii.evalf()
print(str(solution) + " cm")

#plot the function
sympy.plot(attenuation_law, (x, 0, 10), ylabel='attenuation(x)')


