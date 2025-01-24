import pandas as pd
import matplotlib.pyplot as plt


# Set working directory as the current one
import os
os.chdir(os.path.dirname(__file__))

# File paths
temperature_file = 'Group06_temperatureDistribution.csv'
heat_flux_file = 'Group06_normalizedHeatFlux.csv'
literature_results_file = 'literature_results.csv'

# Load the data
temperature_data = pd.read_csv(temperature_file)
heat_flux_data = pd.read_csv(heat_flux_file)
literature_results = pd.read_csv(literature_results_file)

# Rename columns for better readability
temperature_data.columns = ['Depth (m)', 'Temperature (°C)']
heat_flux_data.columns = ['Depth/Pool Height', 'Normalized Heat Flux']
literature_results.columns = ['Depth (m)', 'Temperature (°C)']


# CFD Data
x_CFD = []
y_CFD = []
with open('vertical temperature 5', 'r') as file:
    for line in file:
        if line.strip():
            x, y = map(float, line.split())
            x_CFD.append(x)
            y_CFD.append(y)

import numpy as np
y_CFD = np.array(y_CFD) - 273.15
x_CFD = 2 - np.array(x_CFD)


# Plot normalized heat flux
plt.figure(figsize=(10, 6))
plt.scatter(heat_flux_data['Depth/Pool Height'], heat_flux_data['Normalized Heat Flux'], marker='s', color='r', label='Normalized Heat Flux')
plt.xlabel('Depth/Pool Height')
plt.ylabel('Normalized Heat Flux')
plt.title('Normalized Heat Flux vs Depth/Pool Height')
plt.legend()
plt.grid(True)
plt.show()

# Compute and display average temperature
average_temperature = temperature_data['Temperature (°C)'].mean() + 273.15
print(f"Average Temperature on the vertical line: {average_temperature:.2f} K ({average_temperature-273.15:.2f} °C)")

Ra_int = 2.36e16
H = 2
V_pool = 3.14*H**2/4 * 0.15
R_v = (4*V_pool/(3.14*H))**0.5
Nu_dn = 0.116 * (H / R_v)**0.32 * Ra_int ** 0.25
alpha = Nu_dn * 0.6 / H
Area = 3.14 * 2 * 0.15 /4
power = 15e3
T_delta = power / (alpha * Area)
T_bulk = T_delta + 273.15
print(f"Average Bulk Temperature: {T_bulk:.2f} K, {T_bulk-273.15:.2f} °C")




# Plot temperature distribution
plt.figure(figsize=(10, 6))
plt.plot(temperature_data['Depth (m)'], temperature_data['Temperature (°C)'], marker='o', label='Temperature Distribution')
# horizontal line at the average bulk temperature
plt.axhline(y=average_temperature-273.15, color='r', linestyle='--', label='Experimental Average Temperature')
plt.axhline(y=T_bulk-273.15, color='b', linestyle='--', label='Computed Bulk Temperature')
plt.plot(literature_results['Depth (m)'], literature_results['Temperature (°C)'], marker='x', color='g', label='Literature Results with AHFM Sharma et al. (2022)')
plt.plot(x_CFD, y_CFD, color='y', label='CFD Data', marker='d')
plt.xlabel('Depth (m)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Distribution vs Depth')
plt.legend()
plt.grid(True)
plt.show()

