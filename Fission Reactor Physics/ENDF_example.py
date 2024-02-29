import matplotlib.pyplot as plt
import ENDF_requests as ENDF

## Example of use of the ENDF module

## The user has to provide the target, reaction and quantity of interest
## The module will return the available data for the user to select from
## The user will then select the PenSectID and the module will return the data
## The user can then plot the data

#as a string
#ELEMENT-MASSNUMBER
#e.g. "U-235", "Pu-239", "Th-232"
target = "U-235"

#it accepts both INTEGERS of the MT code and STRINGS of the reaction name
#MT 1 = n,tot = total cross section
#MT 2 = n,el = elastic scattering
#MT 18 = n,f = total fission
#MT 102 = n,g = radiative capture
#more at https://www-nds.iaea.org/exfor/helpe/help_reaction.htm
reaction = 2
# THESE WON'T WORK:
#MT 452 = N,nu = Average number of TOT neutrons released per fission event
#MT 455 = N,nu_d = Average number of delayed neutrons released per fission event.
#MT 456 = N,nu_p = Average number of prompt neutrons released per fission event

#quantity of interest
#SIG = cross section
#more at https://www-nds.iaea.org/exfor/helpe/help_quantity.htm
#FUNCTIONS NOT READY TO HANDLE DIFFERENT QUANTITIES
quantity = "SIG"

#prinnts the url for the call to the database
print(ENDF.database_call(target, reaction, quantity))

#prints database information to hav e list of PenSectID to choose from, the date of publishing and the authors are also shown
ENDF.database_info(target, reaction, quantity)

#ask the user for the PenSectID from the list shown in the terminal
dataID = input("Please select a PenSectID from the list above: ")

#gets cross section data from the selected dataset
#you can add an optional argument to print more information regarding the retrival of the data
# 1 = print all the raw data
# 2 = print the columns (DATA and Units of Meas.) and the number of points
# if no optional arguments are set the function runs silently
E_values, Sig_values = ENDF.data_get(dataID, 1)

# Plot E vs Sig
plt.plot(E_values, Sig_values)
plt.xlabel('Energy [eV]')
plt.ylabel('Cross-section [b]')
plt.yscale('log')
plt.xscale('log')
plt.grid()
plt.show()


#https://www-nds.iaea.org/exfor/servlet/E4sGetIntSection?SectID=19172580&req=44419&e4up=0&PenSectID=24020191&pen=0
