import numpy as np
import matplotlib.pyplot as plt
import nuclei_func as nf
############################################################################################################
# Exercise 2
############################################################################################################
#Consider the fission spectrum which is given Plot it
#Then write code to ITERATIVELY calculate the fraction of neutron born with:
#    • Energy higher than 10 MeV
#    • Energy lower than 0.1 MeV

Max_Energy = 20 # Maximum energy in MeV
Energy = np.linspace(0, Max_Energy, 10000) # Energy domain in MeV

def spectrum(Energy):
    return 0.453 * np.exp(-1.036 * Energy) * np.sinh(np.sqrt(2.29*Energy)) # Fission spectrum, given formula

spect = spectrum(Energy)

############################################################################################################
# Plot
############################################################################################################
plt.figure()
plt.plot(Energy, spect)
plt.title("Fission Spectrum")
plt.xlim(0, 20)
plt.ylim(0, 0.5)
plt.xlabel(r"$E [MeV]$")
plt.ylabel(r"$\chi(E)$")
plt.grid()
plt.savefig(".\Fission Reactor Physics\Homework1\Sol_2.png")
plt.show()

############################################################################################################
# Several approaches to calculate the fractions
############################################################################################################

# If the energy step is small enough, you can just sum the values
f_high = np.sum(spect[Energy > 10])
f_low = np.sum(spect[Energy < 0.1])
f_tot = np.sum(spect)
print(f"By sum: Fraction E>10 MeV: {(f_high/f_tot)*100}%, Fraction E<0.1 MeV: {(f_low/f_tot)*100}%")

# DIY trapz function, using arrays
def integral(a,b,num):
    step = (b-a)/num
    left_points = np.arange(a,b-step, step)
    right_points = np.arange(a+step,b, step)

    Sol = sum((spectrum(left_points) + spectrum(right_points))*step/2)
    return Sol
f_high = integral(10,Max_Energy,1000)
f_low = integral(0,0.1,1000)
f_tot = integral(0,Max_Energy,1000)
print(f"DIY array: Fraction E>10 MeV: {(f_high/f_tot)*100}%, Fraction E<0.1 MeV: {(f_low/f_tot)*100}%")

# DIY trapz function, using for loop
def integral(a,b,num):
    step = (b-a)/num
    Sol = 0
    for i in range(num):
        E_low = a + i*step
        E_high = a + (i+1)*step
        Sol += (spectrum(E_low) + spectrum(E_high))*step/2
    return Sol
f_high = integral(10,Max_Energy,1000)
f_low = integral(0,0.1,1000)
f_tot = integral(0,Max_Energy,1000)
print(f"DIY loop: Fraction E>10 MeV: {(f_high/f_tot)*100}%, Fraction E<0.1 MeV: {(f_low/f_tot)*100}%")

# Using numpy trapz function
f_high = np.trapz(spect[Energy > 10], Energy[Energy > 10])
f_low = np.trapz(spect[Energy < 0.1], Energy[Energy < 0.1])
f_tot = np.trapz(spect, Energy)
print(f"numpy trapz: Fraction E>10 MeV: {(f_high/f_tot)*100}%, Fraction E<0.1 MeV: {(f_low/f_tot)*100}%")

############################################################################################################
# Now just Print the results in a text file
############################################################################################################

# Normalize the fractions
f_high /= f_tot
f_low /= f_tot

# cut the number to 4 decimal places
f_high = round(f_high, 4)
f_low = round(f_low, 4)

# Save the results in a text file
str0 = "Solution to Exercise 2:\n"
str1 = "Fraction of neutrons born with energy higher than 10 MeV: " + str(f_high*100) + "% \n"
str2 = "Fraction of neutrons born with energy lower than 0.1 MeV: " + str(f_low*100) + "% \n"
text = str0 + str1 + str2
#write the text to a file
with open(".\Fission Reactor Physics\Homework1\Sol_2.txt", "w") as f:
    f.write(text)