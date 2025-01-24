import os
import numpy as np
import matplotlib.pyplot as plt
import csv

# Process experimental data
input_file = "./CFD for Nuclear Engineering/Project - Two Phase/04 - Postprocess/plot-data.csv"
x_experimental, y_experimental = [], []
with open(input_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        x_experimental.append(float(row[0]) / 1000)
        y_experimental.append(float(row[1]))

# Second dataset (test files)
test_folder_path = './CFD for Nuclear Engineering/Project - Two Phase/04 - Postprocess/'
x_values_all = []
y_values_all = []

# Read and combine data from all test_ files
time_steps = 0
for file_name in sorted(os.listdir(test_folder_path)):
    if file_name.startswith("test_"):
        file_path = os.path.join(test_folder_path, file_name)
        time_steps += 1
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    x, y = map(float, line.split())
                    x_values_all.append(abs(x))
                    y_values_all.append(1 - y)

# Convert to NumPy arrays and sort by x-values
x_values_all = np.array(x_values_all)
y_values_all = np.array(y_values_all)
sorted_indices = np.argsort(x_values_all)
x_values_all = x_values_all[sorted_indices]
print(x_values_all)
y_values_all = y_values_all[sorted_indices]

# Perform neighbor averaging with sequential processing
range_width = 0.02
x_averaged = []
y_averaged = []
std_deviation = []

# Start processing from the first x value
i = 0
while i < len(x_values_all):
    # Define the range for averaging
    x_start = x_values_all[i]
    x_end = x_start + range_width

    # Find all points within the range
    neighbors = [j for j, x_val in enumerate(x_values_all) if x_start <= x_val < x_end]
    
    # If no neighbors are found (unlikely in sorted data), skip
    if not neighbors:
        i += 1
        continue

    # Calculate averages for x and y and the standard deviation for y
    neighbor_x_values = [x_values_all[j] for j in neighbors]
    neighbor_y_values = [y_values_all[j] for j in neighbors]
    x_averaged.append(np.mean(neighbor_x_values))
    y_averaged.append(np.mean(neighbor_y_values))
    std_deviation.append(np.std(neighbor_y_values)/2)

    # Move to the next x value outside the current range
    i = neighbors[-1] + 1


# Plot
plt.figure(figsize=(10, 7))

# Experimental Data
plt.scatter(x_experimental, y_experimental, color='red', label="Experimental Data")
print(np.mean(y_experimental))

# CFD Results
plt.errorbar(x_averaged, y_averaged, yerr=std_deviation, fmt='o', capsize=5, label=f"CFD Data avg of {time_steps} time steps", color='blue')
print(np.mean(y_averaged))

# Formatting the plot
plt.xlabel("Radius [m]")
plt.ylabel("Average Volume Fraction")
plt.title("Combined Volume Fraction vs. Radius")
plt.xlim(0, 0.25)
plt.grid(True)
plt.legend()
plt.show()
