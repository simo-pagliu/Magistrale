import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = np.load("System_Availability_and_Reliability.npz")

# Create the first figure for availability
plt.figure(1)
plt.errorbar(data['TIME_AXIS'], data['Availability_Values'], yerr=data['Availability_Error'], label='Availability', linestyle='--', linewidth=0.15)
plt.title("System Availability Over Time")
plt.legend()
plt.xlabel("Time [hours]")
plt.grid()

# Create the second figure for reliability
plt.figure(2)
plt.errorbar(data['TIME_AXIS'], data['Reliability_Values'], yerr=data['Reliability_Error'], label='Reliability', linestyle='--', linewidth=0.15)
plt.title("System Reliability Over Time")
plt.legend()
plt.xlabel("Time [hours]")
plt.grid()

# Show both figures
plt.show()