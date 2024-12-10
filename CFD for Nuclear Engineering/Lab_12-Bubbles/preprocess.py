# 2 phase flow
# mono-disperse homogeneus bubble flow
# we have to eval the holdup
# superficial gas velcoity = 0.01 m/s at the gas outlet
# superficial liquid velocity = 0.00 m/s at the liquid inlet
# the pipe is
# 1 m high
# rectangular cross section: 0.1 m x 0.02 m

height = 1
width = 0.1
depth = 0.02

#Hydraulic diameter
cross_section = width * depth
wetted_perimeter = 2 * width + 2 * depth
hydraulic_diameter = 4 * cross_section / wetted_perimeter
print("Hydraulic diameter: ", hydraulic_diameter)

#Superficial velocities
superficial_gas_velocity = 0.01
area_sparger = 0.0002 #m2
gas_volume_flow_rate = superficial_gas_velocity * cross_section
density = 1.225 #kg/m3
mass_flow_rate = gas_volume_flow_rate * density
print("Mass flow rate: ", mass_flow_rate)