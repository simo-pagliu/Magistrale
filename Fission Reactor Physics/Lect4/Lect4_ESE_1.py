#import modules useful for solving differential equations, use laplace transform, and plot the results
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

#define constants
T_iodine = 6.57 #hours
T_xenon = 9.14 #hours

convertion = lambda tau: np.log(2)/(tau*3600) #convertion from hours to seconds and computatuiin of deacy constant

Lambda_Iodine = convertion(T_iodine) #decay constant for iodine
Lambda_Xenon = convertion(T_xenon) #decay constant for xenon

Iodine_0 = 1 #initial iodine concentration
Xenon_0 = 0 #initial xenon concentration
Cesium_0 = 0 #initial cesium concentration

def Iodine(t, Iodine_0):
    Iodine = Iodine_0 * np.exp(-Lambda_Iodine*t)
    return Iodine

def Xenon(t, Iodine_0, Xenon_0):
    coeffA = Lambda_Iodine*Iodine_0 / (Lambda_Iodine - Lambda_Xenon)
    paramI_decay = np.exp(-Lambda_Iodine*t)
    paramXe_decay = np.exp(-Lambda_Xenon*t)

    Xenon = Xenon_0*paramXe_decay + coeffA*(paramXe_decay - paramI_decay)

    return Xenon

def Cesium(t, Iodine_0, Xenon_0, Cesium_0):
    coeffB = Lambda_Xenon / (Lambda_Xenon - Lambda_Iodine)
    coeffC = Lambda_Iodine / (Lambda_Xenon - Lambda_Iodine)
    paramI_decay = np.exp(-Lambda_Iodine*t)
    paramXe_decay = np.exp(-Lambda_Xenon*t)

    Cesium = Xenon_0*(1 - paramXe_decay) + Iodine_0*(1 - coeffB*paramI_decay + coeffC*paramXe_decay)
    return Cesium

#plot the results
t_i = 0
t_f = 3*24*3600
t_plot = np.linspace(t_i, t_f, 1000)

Iodine_vect = Iodine(t_plot, Iodine_0)
Xenon_vect = Xenon(t_plot, Iodine_0, Xenon_0)
Cesium_vect = Cesium(t_plot, Iodine_0, Xenon_0, Cesium_0)

plt.plot(t_plot, Iodine_vect, label='Iodine')
plt.plot(t_plot, Xenon_vect, label='Xenon')
plt.plot(t_plot, Cesium_vect, label='Cesium')
plt.xlabel('Time (seconds)')
plt.ylabel('Concentration')
plt.legend()
plt.show()

#it then goes on, but again, it's quite pointless to just give the solution to the problem
#check Lect4_ESE_1_VAR.py to see how to solve it with python
