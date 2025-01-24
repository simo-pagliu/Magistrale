# Volume flow rate
volume_flow_rate = 1000 # L/min
volume_flow_rate = volume_flow_rate / (1000*60) # m^3/s
print(f"Volume flow rate: {volume_flow_rate} m^3/s")

# Mass flow rate
rho_air = 1.225 # kg/m^3
mass_flow_rate = volume_flow_rate * rho_air
print(f"Mass flow rate: {mass_flow_rate} kg/s")
small_bubble_percentage = 7/100
large_bubble_percentage = 93/100
print(f"Small bubble mass flow: {(small_bubble_percentage*mass_flow_rate):.4f}kg/s")
print(f"Large bubble mass flow: {(large_bubble_percentage*mass_flow_rate):.4f}kg/s")

# Passage area
diameter = 0.5 #m
radius = diameter/2
area = 3.14 * radius**2

# Velocity
velocity = volume_flow_rate / area
print(f"Velocity: {velocity} m/s")

# Eval distance
cell_dim = 20e-3
velocity = 0.4
char_time = cell_dim / velocity
print(f"Characteristic time: {char_time} s")
print(f"1/4 Characteristic time: {char_time/4} s")
print(f"1/10 Characteristic time: {char_time/10} s")


# Hydraulic diameter
D_h = 4 * area / (2 * 3.14 * radius)
print(f"Hydraulic diameter: {D_h} m")



####
# Check if we can have slugs
rho_water = 998 # kg/m^3
D_star = diameter / (0.072 / (9.81 * (rho_water - rho_air)))**0.5
print(f"D_star: {D_star:.2f}")


small_bubble_diameter = 4.8e-3
large_bubble_diameter = 12.9e-3

Eotvos_small = 9.81 * (rho_water - rho_air) * small_bubble_diameter**2 / 0.072
print(f"Eotvos number for small bubble: {Eotvos_small:.2f}")

Eotovs_large = 9.81 * (rho_water - rho_air) * large_bubble_diameter**2 / 0.072
print(f"Eotvos number for large bubble: {Eotovs_large:.2f}")




