import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

########################################################
# Load the data from the CSV file
########################################################
# Load the CSV data
csv_file_path = 'Re133000_velocityProfile.csv'
csv_data = pd.read_csv(csv_file_path)

# Define R_pipe and maximum velocity scaling factor
R_pipe = np.sqrt(0.001955371/np.pi)
bulk_v = 39.74365 # area weighted average of the velocity profile

# Prepare the original data from 0 to R
x_csv = csv_data['y/R'] * R_pipe
y_csv = csv_data['U/Ub'] * bulk_v

# Convert to numpy arrays
x_csv = x_csv.to_numpy()
y_csv = y_csv.to_numpy()

x_csv = np.concatenate([x_csv - x_csv[-1], np.flip(x_csv[-1] - x_csv)])
y_csv = np.concatenate([y_csv, np.flip(y_csv)])

########################################################
# Load the data from the ANSYS output file
########################################################
x = []
y = []
with open('data', 'r') as file:
    for line in file:
        if line.strip() and not line.startswith(("#", "(", ")")):
            x_val, y_val = map(float, line.split())
            x.append(x_val)
            y.append(y_val)

# Plot both datasets
# Plot the combined data
plt.figure(figsize=(8, 6))
plt.plot(x_csv, y_csv, label='CSV Data', marker='o')
plt.plot(x, y, label='Ansys', marker='o')
plt.xlabel('Position (m)')
plt.ylabel('Velocity Magnitude (m/s)')
plt.title('Velocity Magnitude Comparison')
plt.legend()
plt.grid(True)
plt.show()
