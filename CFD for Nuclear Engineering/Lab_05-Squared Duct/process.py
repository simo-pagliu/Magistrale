# Given Data
Re = 40000
density = 1.225 #kg/m3
viscosity = 1.789e-5 #kg/m.s

# Choose a pipe of 1m diameter
half_height = 1.0 #m

# Calculations
velocity = Re * viscosity / (density * 2*half_height)
print("Velocity: ", velocity, "m/s")

mass_flow_rate = density * velocity * (2*half_height)**2
print("Mass flow rate: ", mass_flow_rate, "kg/s")