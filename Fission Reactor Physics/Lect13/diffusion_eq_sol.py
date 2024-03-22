################################################
# Import the necessary libraries
################################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # 3D plotting :)
import matplotlib.animation as animation

################################################
# Meshgrid example
################################################

Num = 1000
x_lim_sup = 20
x_vect = np.linspace(0.001, x_lim_sup, Num)
mu_vect = np.linspace(0.001, 1, Num)

C_o = 1
sigma_abs = 0.1

# define a new function
def flux(x, mu):
    Sol = C_o * np.exp(-sigma_abs * x / mu)
    return Sol

x_vals, y_vals = np.meshgrid(x_vect, mu_vect) # create a meshgrid

plt.contourf(x_vals, y_vals, flux(x_vals, y_vals),levels = 20, cmap='jet')
plt.colorbar(label = r'$\varphi(x,\mu)$')
plt.ylabel(r'$\mu$')
plt.xlabel(r'$x$')
plt.grid(True,linestyle = '--')
plt.show()

################################################
# Animated plot, varying the angle of scattering
################################################

fig, ax = plt.subplots()
steps = 20
mu = np.linspace(0.1, 1, steps)
flux_anim = flux(x_vect, mu[0])
# create a line plot as the first frame
line2 = ax.plot(x_vect[0], flux_anim[0])[0]
# set the axis labels
ax.set(xlim=[0, x_lim_sup], ylim=[0, 1], xlabel=r'$x$', ylabel=r'$\varphi(x,\mu)$')
ax.legend(f'mu = {mu[0]}')

# define a vector of colors
colors = plt.cm.jet(np.linspace(0, 1, steps))

def update(frame):
    # update the line plot:
    line2.set_xdata(x_vect)
    line2.set_ydata(flux(x_vect, mu[frame]))
    line2.set_color(colors[frame])  # update the line color
    ax.legend([fr'$\mu$ = {mu[frame]:.2f}'])

    return (line2, ax)


ani = animation.FuncAnimation(fig=fig, func=update, frames=steps, interval=100)
plt.show()

################################################
# Animated plot, varying the position
################################################

fig, ax = plt.subplots()
steps = 10
x_vect = np.linspace(10, 1, steps)
mu = np.linspace(0.001, 1, Num)
flux_anim = flux(x_vect[0], mu)
# create a line plot as the first frame
line2 = ax.plot(x_vect[0], flux_anim[0])[0]
# set the axis labels
ax.set(xlim=[0, 1], ylim=[0, 1], xlabel=r'$\mu$', ylabel=r'$\varphi(x,\mu)$')
ax.legend(f'x = {x_vect[0]} cm')

# define a vector of colors
colors = plt.cm.jet(np.linspace(0, 1, steps))

def update(frame):
    # update the line plot:
    line2.set_xdata(mu)
    line2.set_ydata(flux(x_vect[frame], mu))
    line2.set_color(colors[frame])  # update the line color
    ax.legend([fr'$x$ = {x_vect[frame]:.2f} cm'])

    return (line2, ax)


ani = animation.FuncAnimation(fig=fig, func=update, frames=steps, interval=150)
plt.show()

################################################
# 3D plot
################################################

source = 1
# define a new function
def flux(x, mu):
    Sol = (source/(4*np.pi*mu))*np.exp(-sigma_abs*x/mu)
    return Sol

steps = 1000
x_vals, y_vals = np.meshgrid(
    np.linspace(0,0.05,steps),
    np.linspace(0.001,1,steps))

plot = plt.figure()
AX = plot.add_subplot(111, projection = '3d')
S = AX.plot_surface(x_vals,y_vals,flux(x_vals,y_vals),cmap = 'jet')
AX.set_xlabel('x (cm)')
AX.set_ylabel(r'$\mu$')
AX.set_zticks([])
plot.colorbar(S,label = r'$\varphi(x,\mu)$')
plt.tight_layout()
plt.show()
