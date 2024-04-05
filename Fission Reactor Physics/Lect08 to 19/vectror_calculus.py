#I want to try to perform some vector calculus operations using python
#I will use numpy to perform the operations
import numpy as np
#I will use the math package to perform some operations
import sympy as sp
#I will use the matplotlib package to plot the results
import matplotlib.pyplot as plt

#define an array
n = sp.CoordSys3D('N')
#I will define a vector
v = 3*n.i + 4*n.j + 5*n.k
#I will define another vector
w = 6*n.i + 7*n.j + 8*n.k

print('The product of the vectors is:', v*w)
print('The dot product of the vectors is:', v.dot(w))
print('The cross product of the vectors is:', v.cross(w))

#v.factor()
#v.simplify()
