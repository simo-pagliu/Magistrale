import os
import numpy as np

x_coordinates = []
water_vof_values = []

# Specify the folder path
folder_path = "./CFD for Nuclear Engineering/Project - Two Phase/03 - Simulation/data_vol_frac"  # Replace with the folder containing your files

# Loop through all files in the folder
i = 0
for file_name in sorted(os.listdir(folder_path)):
    i += 1
    if file_name.startswith("vol_frac_water"):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Temporary storage for water-vof values from this file
        temp_water_vof = []

        for line in lines:
            if "nodenumber" in line or not line.strip():
                continue

            parts = line.split(',')
            x_coordinate = float(parts[1])
            water_vof = float(parts[-1])

            # Store x-coordinates (only once, from the first file)
            if len(x_coordinates) < len(lines) - 1:
                x_coordinates.append(x_coordinate)

            temp_water_vof.append(water_vof)

        # Append water_vof from this file to the main list
        water_vof_values.append(temp_water_vof)

print("Number of files processed:", i)

# Convert the water_vof_values to a NumPy array for easier processing
water_vof_array = np.array(water_vof_values)

# Calculate the average and standard deviation along the columns (i.e., for each point)
avg_water_vof = np.mean(water_vof_array, axis=0)
avg_air_vof = 1 - avg_water_vof
std_water_vof = np.std(water_vof_array, axis=0)

# DEBUG
# print("x_coordinates:", x_coordinates)
# print("avg_water_vof:", avg_water_vof)
# print("std_water_vof:", std_water_vof)

#plot

import matplotlib.pyplot as plt

plt.errorbar(x_coordinates, avg_air_vof, yerr=std_water_vof, fmt='o', capsize=5)
plt.xlabel("x-coordinate")
plt.ylabel("Average Volume Fraction")
plt.title("Average Volume Fraction vs. x-coordinate")
plt.xlim(-0.25,0.25)
plt.grid(True)
plt.show()