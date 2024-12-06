# DATA (air @ 350K)
rho = 1.024
mu = 2.018e-5
cp = 1008
alpha = 2.5e-5
k = 0.026
beta = 3.4e-3
g = 9.81
delta_T = 373 - 327
L = (46.3-17.8)/1000

# prundl number
Pr = mu*cp/k

# Rayleigh number
Ra = g*beta*delta_T*L**3/(mu*alpha)
print('Prundl number: ', Pr)
print('Rayleigh number: ', Ra)