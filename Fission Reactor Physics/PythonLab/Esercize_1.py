#import numpy and plot
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

#Data given 

Tau_Iodine = 6.57 #hours
lambda_Iodine = np.log(2)/(Tau_Iodine*3600)

Tau_Xenon = 9.14 #hours
lambda_Xenon = np.log(2)/(Tau_Xenon*3600) 

Yield_Iodine = 0.0639
Yield_Xenon = 0.00237

#Initial conditions, normalized to Iodine concentration
Rate_Fission = 9.34e19
Rate_Capture = 8.1e-5
Iodine_0 = 1
Xenon_0 = 0

#cross sections
Iodine_fission_cross_sec = 1 #TEMP


#Time 
t_i = 0
t_stop = 24*3600*4 #4 days, then scrammed
t_1 = np.linspace(t_i,t_stop,1000) #from startup to scram
t_scrammed = t_stop + 24*3600*2 #2 days off
t_2 = np.linspace(t_stop, t_scrammed, 1000) #from scram to criticality
t_f = t_scrammed + 24*3600*10 #10 days of criticality
t_3 = np.linspace(t_scrammed, t_f, 1000) #from scrammed to full power


#OMISSIS: the actual solution, just plot it, because why not...
t = sp.symbols('t')
Iodine = sp.Function('Iodine')(t)
Xenon = sp.Function('Xenon')(t)
Cesium = sp.Function('Cesium')(t)
eq1 = sp.Eq(Iodine.diff(t), -lambda_Iodine*Iodine + Rate_Fission*Yield_Iodine*Iodine_fission_cross_sec) 
eq2 = sp.Eq(Xenon.diff(t), -lambda_Xenon*Xenon + lambda_Iodine*Iodine)
eq3 = sp.Eq(Cesium.diff(t), lambda_Xenon*Xenon)

#solve the sistem of differential equations with the initial conditions
initial_conditions={Iodine.subs(t, 0): Iodine_0, Xenon.subs(t, 0): Xenon_0, Cesium.subs(t, 0): Cesium_0}
sol = sp.dsolve((eq1, eq2, eq3), ics=initial_conditions)
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

#Vectors of concentrations values
Iodine_vect = []
Xenon_vect = []

#solution during time interval t_1
Iodine_t1 = Iodine(t_1, Rate_Fission, Rate_Capture, Iodine_0, Xenon_0)
Xenon_t1 = Xenon(t_1, Rate_Fission, Rate_Capture, Iodine_0, Xenon_0)
#solution during time interval t_2
Iodine_t2 = Iodine(t_1, 0, 0, Iodine_t1[-1], Xenon_t1[-1])
Xenon_t2 = Xenon(t_1, 0, 0, Iodine_t1[-1], Xenon_t1[-1])
#solution during time interval t_3
Iodine_t3 = Iodine(t_1, Rate_Fission, Rate_Capture, Iodine_t2[-1], Xenon_t2[-1])
Xenon_t3 = Xenon(t_1, Rate_Fission, Rate_Capture, Iodine_t2[-1], Xenon_t2[-1])

#Concatenation of the vectors
Iodine_vect = np.concatenate((Iodine_t1, Iodine_t2, Iodine_t3))
Xenon_vect = np.concatenate((Xenon_t1, Xenon_t2, Xenon_t3))
t_vect = np.concatenate((t_1, t_2, t_3))

#Plot
plt.plot(t_vect/3600, Iodine_vect, label='Iodine Concentration')
plt.plot(t_vect/3600, Xenon_vect, label='Xenon Concentration')
plt.legend()
plt.xlabel("time [h]")
plt.ylabel("Concentration normalized")
plt.grid()
plt.show()




