import pandas as pd
import matplotlib.pyplot as plt


# Set working directory as the current one
import os
os.chdir(os.path.dirname(__file__))

# File paths
temperature_file = 'Group06_temperatureDistribution.csv'
heat_flux_file = 'Group06_normalizedHeatFlux.csv'

# Load the data
temperature_data = pd.read_csv(temperature_file)
heat_flux_data = pd.read_csv(heat_flux_file)

# Rename columns for better readability
temperature_data.columns = ['Depth (m)', 'Temperature (°C)']
heat_flux_data.columns = ['Depth/Pool Height', 'Normalized Heat Flux']

# Plot temperature distribution
plt.figure(figsize=(10, 6))
plt.plot(temperature_data['Depth (m)'], temperature_data['Temperature (°C)'], marker='o', label='Temperature Distribution')
plt.xlabel('Depth (m)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Distribution vs Depth')
plt.legend()
plt.grid(True)
plt.show()

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
print(f"Average Temperature: {average_temperature:.2f} K")
