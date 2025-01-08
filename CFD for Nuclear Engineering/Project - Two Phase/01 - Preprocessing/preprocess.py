# Volume flow rate
volume_flow_rate = 1000 # L/min
volume_flow_rate = volume_flow_rate / (1000*60) # m^3/s
print(f"Volume flow rate: {volume_flow_rate} m^3/s")

# Mass flow rate
rho_air = 1.225 # kg/m^3
mass_flow_rate = volume_flow_rate * rho_air
print(f"Mass flow rate: {mass_flow_rate} kg/s")

# Passage area
diameter = 0.04 #m
radius = diameter/2
area = 3.14 * radius**2

# Velocity
velocity = volume_flow_rate / area
print(f"Velocity: {velocity} m/s")

# Eval distance
cell_dim = 15e-3 #m
char_time = cell_dim / velocity
print(f"Characteristic time: {char_time} s")



