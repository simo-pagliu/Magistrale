import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Plot stramwise variance y

########################################################
# Load the data from the CSV file
########################################################
# Load the CSV data
csv_file_path = 'axialVariace.csv'
csv_data = pd.read_csv(csv_file_path)

# Prepare the original data from 0 to R
x_csv = csv_data['y+']
y_csv = csv_data['uz2/utau2']

# Convert to numpy arrays
x_csv = x_csv.to_numpy()
y_csv = y_csv.to_numpy()

# x_csv = np.concatenate([x_csv - x_csv[-1], np.flip(x_csv[-1] - x_csv)])
# y_csv = np.concatenate([y_csv, np.flip(y_csv)])

########################################################
# Load the data from the ANSYS output file
########################################################
x = []
y = []
fluid_density = 1.225
fluid_viscosity = 1.7894e-05
friciton_velocity = 1.79
with open('streamwise-var-y', 'r') as file:
    for line in file:
        if line.strip() and not line.startswith(("#", "(", ")")):
            x_val, y_val = map(float, line.split())
            x_val_mod = friciton_velocity/fluid_viscosity * (x_val+0.0249791) * fluid_density
            x.append(x_val_mod)
            y_val_mod = y_val / friciton_velocity**2 
            y.append(y_val_mod)

len_x = len(x)
len_x_half = int(len_x/2)

# Plot both datasets
# Plot the combined data
plt.figure(figsize=(8, 6))
plt.semilogx(x_csv, y_csv, label='CSV Data', marker='o')
plt.semilogx(x[0:len_x_half], y[0:len_x_half], label='Ansys', marker='o')
plt.xlabel('y+')
plt.ylabel('u_z^2/u_tau^2')
plt.title('Comparison')
plt.legend()
plt.grid(True)
plt.show()
