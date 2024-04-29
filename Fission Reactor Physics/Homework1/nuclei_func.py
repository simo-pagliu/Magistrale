############################################################################################################
# NUCLEI FUNCTIONS
#
# This file contains a collection of functions related to nuclear physics and reactions.
# Each function serves a specific purpose and can be used independently or in combination with others.
# The functions in this file are designed to perform calculations and provide useful information
# for studying and analyzing nuclear phenomena.
#
# Author: [Pagliuca Simone]
# Date: [18/04/2024]
#
############################################################################################################
import inspect



############################################################################################################
# Function to calculate the macroscopic cross section from the microscopic cross section
############################################################################################################
def macro(micro_sigma, density, molar_mass):
    N_a = 6.022e23 # Avogadro's number
    barn = 1e-24 # b-->cm2
    macro_sigma = micro_sigma * N_a * density / molar_mass * barn
    return macro_sigma

############################################################################################################
# Function to calculate the cross section of a mixture
############################################################################################################
def mixture(quantity, quality, normalization_cond='no_normalize'):

    #check if the quantity and quality lists have the same length
    if len(quantity) != len(quality): 
        print("The quantity and quality lists must have the same length.")
        return None

    #check if the sum of the quality values is equal to 1, if not, ask the user if they want to normalize them
    if sum(quality) != 1:
        if normalization_cond == 'normalize':
            quality = [q/sum(quality) for q in quality]
        elif normalization_cond == 'no_normalize':
            print(f"\033[93mThe sum of the qualites values is not 1, at line {inspect.currentframe().f_back.f_lineno}, default behaviour is ignoring.\033[0m")  
    
    #calculate the macroscopic cross section of the mixture
    mixture_val = sum([quantity[i]*quality[i] for i in range(len(quantity))])
    return mixture_val

############################################################################################################
# From weight percentage to molar fraction
############################################################################################################
def w2mol(weight_fraction, molar_mass):

    # check if the weight percentage and atomic weight lists have the same length
    if len(weight_fraction) != len(molar_mass):
        print("The weight percentage and atomic weight lists must have the same length.")
        return None
    
    ans = [] #initialize the molar fraction list
    denominator = sum([weight_fraction[jj]/molar_mass[jj] for jj in range(len(weight_fraction)) ]) #compute the denominator outside the loop
    #loop to calculate the molar fractions
    for ii in range(len(molar_mass)):
        ans.append((weight_fraction[ii]/molar_mass[ii])/denominator)

    return ans

############################################################################################################
# From molar fraction to weight percentage
############################################################################################################
def mol2w(mol_fraction, molar_mass):

    # check if the weight percentage and atomic weight lists have the same length
    if len(mol_fraction) != len(molar_mass):
        print("The weight percentage and atomic weight lists must have the same length.")
        return None
    
    ans = [] #initialize the weight fraction list
    denominator = sum([mol_fraction[jj]*molar_mass[jj] for jj in range(len(mol_fraction)) ]) #compute the denominator outside the loop
    #loop to calculate the molar fractions
    for ii in range(len(molar_mass)):
        ans.append((mol_fraction[ii]*molar_mass[ii])/denominator)

    return ans

############################################################################################################
# From volumetric percentage to weight fraction
############################################################################################################
def vol2w(volume_fraction, density):

    # check if the weight percentage and atomic weight lists have the same length
    if len(volume_fraction) != len(density):
        print("The weight percentage and atomic weight lists must have the same length.")
        return None
    
    ans = [] #initialize the molar fraction list
    denominator = sum([volume_fraction[jj]*density[jj] for jj in range(len(volume_fraction))]) #compute the denominator outside the loop
    #loop to calculate the molar fractions
    for ii in range(len(density)):
        ans.append((volume_fraction[ii]*density[ii])/denominator)

    return ans