import numpy as np
import matplotlib.pyplot as plt
import csv
############################################################################################################
# Import data from json file generated in Exercise 9a, and define the variables
############################################################################################################
def import_data(file_path):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        data = {field: [] for field in reader.fieldnames}
        for row in reader:
            for field in reader.fieldnames:
                data[field].append(float(row[field]))
        return data

data = import_data("./Fission Reactor Physics/Homework1/Sol_9.csv")
t_vals = np.array(data["Time [s]"])
U_Sol = np.array(data["U-235 [atoms]"])
Nd_Sol = np.array(data["Nd-140 [atoms]"])
Pm_Sol = np.array(data["Pm-149 [atoms]"])
Sm_Sol = np.array(data["Sm-149 [atoms]"])

# # Normalise the concentrations to the initial U-235 concentration
# norm = U_Sol[0]
# U_Sol /= norm
# Nd_Sol /= norm
# Pm_Sol /= norm
# Sm_Sol /= norm

############################################################################################################
# Plot the concentrations
############################################################################################################
plt.figure()
# plt.plot(t_vals, U_Sol, label='U-235')
plt.plot(t_vals, Nd_Sol, label='Nd-140')
plt.plot(t_vals, Pm_Sol, label='Pm-149')
plt.plot(t_vals, Sm_Sol, label='Sm-149')
plt.xlabel("Time [s]")
plt.ylabel("Concentration [#atoms]")
plt.title("Concentration of isotopes over time")
plt.legend()
plt.grid()
# save the plot to a file
plt.savefig(".\Fission Reactor Physics\Homework1\Sol_9.png")
plt.show()