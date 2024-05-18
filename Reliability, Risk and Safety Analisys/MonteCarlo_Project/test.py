import sympy as sp
import numpy as np

from sympy import init_printing
init_printing(use_unicode=True)

# Define the time variable
t = sp.symbols('t', positive=True, real=True)

# Define the functions
x = sp.Function('x1', positive=True)(t)
y = sp.Function('x2', positive=True)(t)
z = sp.Function('x3', positive=True)(t)
w = sp.Function('x4', positive=True)(t)

# Define some parameters
Lambda = 5.5e-3 #sp.symbols('rate')
mu = 2.2e-1 #sp.symbols('mu')

# Define the matrix of the system 4x4
A = sp.Matrix([[-4*Lambda, 0, mu, 0],
               [4*Lambda, -6*Lambda, 0, mu],
               [0, 6*Lambda, -8*Lambda - mu, 0],
               [0, 0, 8*Lambda, -mu]])

# Define the vector of the system 4x1
X = sp.Matrix([x, y, z, w])

# Define the right-hand side of the system
B = sp.Matrix([sp.diff(x), sp.diff(y), sp.diff(z), sp.diff(w)])

# Define the system of differential equations
# Define the system of differential equations
eqs = A*X - B
print(eqs)

# Extract each equation from the system
eq1 = eqs[0]
eq2 = eqs[1]
eq3 = eqs[2]
eq4 = eqs[3]

# Print the equations
# print("DIOCANE", eq1, eq2, eq3, eq4)

# Solve the system of differential equations, with initial conditions x=1, y=0, z=0, w=0
solution = sp.dsolve(eqs, ics={x.subs(t, 0): 1, y.subs(t, 0): 0, z.subs(t, 0): 0, w.subs(t, 0): 0})
# print(solution)


# # Define system of equations
# eq1 = sp.Eq(-4*Lambda*x + mu*z, sp.diff(x))
# eq2 = sp.Eq(4*Lambda*x - 6*Lambda*y + mu*w, sp.diff(y))
# eq3 = sp.Eq(6*Lambda*y - (8*Lambda + mu)*z, sp.diff(z))
# eq4 = sp.Eq(8*Lambda*z - mu*w, sp.diff(w))

# # Solve the system of differential equations, with initial conditions x=1, y=0, z=0, w=0
# solution = sp.dsolve([eq1, eq2, eq3, eq4], ics={x.subs(t, 0): 1, y.subs(t, 0): 0, z.subs(t, 0): 0, w.subs(t, 0): 0})
# print(solution)

# Extract q1, q2, q3, q4 from the solution
q1 = solution[0].rhs
q2 = solution[1].rhs
q3 = solution[2].rhs
q4 = solution[3].rhs
# print(q1)
# print(q2)
# print(q3)
# print(q4)

# Sum up only success states
availability = q1 + q2 + q3 #q4

###############################################

# Define the time variable
t = sp.symbols('t', positive=True, real=True)

# Define the functions
x = sp.Function('x1', positive=True)(t)
y = sp.Function('x2', positive=True)(t)
z = sp.Function('x3', positive=True)(t)
w = sp.Function('x4', positive=True)(t)

# Define some parameters
Lambda = 5.5e-3 #sp.symbols('rate')
mu = 2.2e-1 #sp.symbols('mu')

# Now solve them again but remove the last column and last row of the matrix A
A = sp.Matrix([[-4*Lambda, 0, mu],
                [4*Lambda, -6*Lambda, 0],
                [0, 6*Lambda, -8*Lambda - mu]])
B = sp.Matrix([sp.diff(x), sp.diff(y), sp.diff(z)])
X = sp.Matrix([x, y, z])
eqs = A*X - B
solution = sp.dsolve(eqs, ics={x.subs(t, 0): 1, y.subs(t, 0): 0, z.subs(t, 0): 0})
# print(solution)

# Extract r1, r2, r3 from the solution
r1 = sp.re(solution[0].rhs)
r2 = sp.re(solution[1].rhs)
r3 = sp.re(solution[2].rhs)
# print(r1)
# print(r2)
# print(r3)

# Sum up
reliability = r1 + r2 + r3

###############################################

# Plot the solution
import matplotlib.pyplot as plt
t_values = np.linspace(0, 1000, 100)

avail_values = np.array([availability.subs(t, value).evalf() for value in t_values])
plt.plot(t_values, avail_values)
plt.xlabel('Time')
plt.ylabel('A(t)')
plt.title('AVAILABILITY')
plt.show()

rely_values = np.array([reliability.subs(t, value).evalf() for value in t_values])
plt.plot(t_values, rely_values)
plt.xlabel('Time')
plt.ylabel('R(t)')
plt.title('RELIABILITY')
plt.show()

