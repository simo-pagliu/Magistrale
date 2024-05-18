import sympy as sp
import numpy as np
import math

REPAIR_RATE = 2.2e-1
FAIL_RATE = 5.5e-3
COMMON_RATE = 1.5e-3
COMMON_PROB = 0.4

A = sp.Matrix([[-4*FAIL_RATE, 0, REPAIR_RATE],
                [4*FAIL_RATE, -6*FAIL_RATE, 0],
                [0, 6*FAIL_RATE, -8*FAIL_RATE - REPAIR_RATE]])

# Define the size of the matrix
n = 3
print(A)
# Populate the matrix
for i in range(n):
    for j in range(n):
        if i != j:
            aaaa = COMMON_RATE * math.comb(4-i, j) * COMMON_PROB**j * (1-COMMON_PROB)**(4-i-j)
            A[i, j] =+ aaaa
            print(i, j, aaaa)

        else:
            A[i, j] =- sum([COMMON_RATE * math.comb(4-i, k) * COMMON_PROB**k * (1-COMMON_PROB)**(4-i-k) for k in range(0, j-1)])

print(A)