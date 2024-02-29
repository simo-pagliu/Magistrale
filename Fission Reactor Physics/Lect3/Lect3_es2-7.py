#exercise 2.7 "due to home" last slide on Lecture 3

#constants
Intensity = 1e12 # n/cm2 sec
cross_sec_tot = 4 #barn

mean_time_before_interaction = 1 / (Intensity * cross_sec_tot*1e-24)
#print mean_time_before_interaction in scientific notation
print(f"{mean_time_before_interaction:.2e}")

#the value is the mean time before interactions for 1 single nucleus, therefore is really small. to have a resaonable value you should multiply it by the Atomic density of a material
