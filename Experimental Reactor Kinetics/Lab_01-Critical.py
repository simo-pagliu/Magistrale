from framework import Measurement as m
from framework import rss
# Define the estimated error for time measurements
estimated_error = 0.5  # Replace with actual estimated error if known

# Structured Data
class MeasurementData:
    def __init__(self):
        self.start = [
            m(128, 1), m(198, 1), m(298, 1), m(348, 1), 
            m(398, 1), m(470, 1), m(520, 1), m(591, 1), m(662, 1), m(740, 1)
        ]
        self.end = [
            m(198, 1), m(298, 1), m(348, 1), m(398, 1), 
            m(470, 1), m(520, 1), m(591, 1), m(662, 1), m(740, 1), m(818, 1)
        ]
        self.time_3_4_5W = [
            m(160, estimated_error), m(24.4, estimated_error), m(44.4, estimated_error),
            m(38.6, estimated_error), m(5.33, estimated_error), m(31, estimated_error),
            m(21, estimated_error), m(28.5, estimated_error), m(47, estimated_error),
            m(141, estimated_error)
        ]
        self.time_6_9W = [
            m(224, estimated_error), m(29, estimated_error), m(50.5, estimated_error),
            m(43.2, estimated_error), m(5.33, estimated_error), m(32.3, estimated_error), m(25, estimated_error),
            m(31.6, estimated_error), m(50.2, estimated_error), m(172, estimated_error)
        ]

# Import
import numpy as np

# Create the data structure
measurement = MeasurementData()

# DATA
# Large lambda value
lambda_big = 5.0E-05

# Lambda values (λ in s⁻¹)
lambda_values = np.array([3.01, 1.14, 0.301, 0.111, 0.0305, 0.0124])

# Beta values (β in -) from the third row
beta_values = np.array([3.07E-04, 8.40E-04, 2.88E-03, 1.43E-03, 1.60E-03, 2.41E-04])

# Output the vectors
# print("Lambda Vector (λ):", lambda_values)
# print("Beta Vector (β):", beta_values)

# Time
w = 0.5 # weight factor
time = w * np.array(measurement.time_6_9W) + (1-w) * np.array(measurement.time_3_4_5W)
rho = []
for i in range(0, len(time)):
    estimated_T = time[i].value / np.log(1.5)
    rho.append( ( lambda_big/estimated_T + sum(beta_values / (1 + estimated_T * lambda_values)) )*100000 )

# Integral reactivity
# Into dollars
beta_pcm_tot = 730
dollar_rho = sum(rho) / beta_pcm_tot
print(f"Total CR worth: {dollar_rho:.2f} $")


# MC simulation with serpent
# Full core critical REG in: 1.06548 +/- 0.00128  [1.06299  1.06798]
# Full core critical REG out: 1.07656 +/- 0.00105  [1.07451  1.07861]
reg_in = m(1.06541, 0.00019) #1.06541 +/- 0.00019
reg_out = m(1.07631, 0.00019) #1.07631 +/- 0.00019

rho_in = rss(lambda k: (k-1)/k, reg_in)
rho_out = rss(lambda k: (k-1)/k, reg_out)

# Compute Control Rod Worth, in dollars
beta = 0.0073
CR_worth = (rho_out - rho_in) / beta
print(f"CR worth from SERPENT Simulation: {CR_worth}$ Interval: ({(CR_worth.value - CR_worth.uncertainty):.2f}$, {(CR_worth.value + CR_worth.uncertainty):.2f}$)")