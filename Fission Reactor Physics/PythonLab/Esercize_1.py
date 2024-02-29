#import numpy and plot
import numpy as np
import matplotlib.pyplot as plt

#Data given 

Tau_Iodine = 6.57 #hours
lambda_Iodine = np.log(2)/(Tau_Iodine*3600)

Tau_Xenon = 9.14 #hours
lambda_Xenon = np.log(2)/(Tau_Xenon*3600) 

Yield_Iodine = 0.0639
Yield_Xenon = 0.00237

#Time 
t_i = 0
t_stop = 3*24*3600
t_f = 4*24*3600
t_vect = np.linspace(t_i,t_f,7*24)
print(t_vect)
print(t_stop)

#OMISSIS: the actual solution, just plot it, because why not...

#Vectors of concentrations values
Iodine_vect = []
Xenon_vect = []

#Concentration of Iodine
def Iodine(t, Rate_Fission, Rate_Capture, Iodine_0, Xenon_0):
    coeffA = Yield_Iodine * Rate_Fission / lambda_Iodine
    paramFiss = 1 - np.exp(-lambda_Iodine * t)
    Iodine = Iodine_0 * np.exp(-lambda_Iodine*t) + coeffA * paramFiss
    return Iodine

#Concentration of Xenon
def Xenon(t, Rate_Fission, Rate_Capture, Iodine_0, Xenon_0):
    coeffA = (Iodine_0*lambda_Iodine - Yield_Iodine*Rate_Fission) / (lambda_Iodine - lambda_Xenon - Rate_Capture)
    paramI = np.exp(-lambda_Iodine*t)
    coeffB = Rate_Fission*(Yield_Iodine + Yield_Xenon)/(lambda_Xenon + Rate_Capture)
    paramXe = np.exp(-lambda_Xenon*t - Rate_Capture*t)

    Xenon = Xenon_0*paramXe + coeffA*(paramXe - paramI) + coeffB*(1 - paramXe)

    return Xenon

#Initial conditions, normalized to Iodine concentration
Rate_Fission = 9.34e19
Rate_Capture = 8.1e-5
Iodine_0 = 1
Xenon_0 = 0

scram = np.where(t_vect > t_stop)
scram = scram[0][1]
#plot Xeonon and Iodine
for ii in range(0,len(t_vect)):

    if ii == scram:
        Iodine_0 = Iodine_vect[-1]
        Xenon_0 = Xenon_vect[-1]
        
        Rate_Fission=0
        Rate_Capture=0

    print(Xenon_0)
    print(Iodine_0)

    Iodine_vect.append(Iodine(t_vect[ii], Rate_Fission, Rate_Capture, Iodine_0, Xenon_0))
    Xenon_vect.append(Xenon(t_vect[ii], Rate_Fission, Rate_Capture, Iodine_0, Xenon_0))

plt.plot(t_vect/3600, Iodine_vect, label='Iodine Concentration')
plt.plot(t_vect/3600, Xenon_vect, label='Xenon Concentration')
plt.legend()
plt.xlabel("time [h]")
plt.ylabel("Concentration normalized")
plt.grid()
plt.show()




