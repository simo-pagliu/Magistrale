# Definition of Main quantities
## Porosity, macroscopic point of view
The total volumetric porosity $n_{V}$ can be defined as
$$
n_V = \frac{V_{void}}{V_{tot}}
$$
Assuming the volume taken in consideration is big enough that is rapresentative of the whole sample ($V > V_{lim}$), this last hypotesis is what sets our studies on the macroscopic point of view.  
In practice we will mostly use the effective porosity $n$ that takes into acount the effective volume composed by the interconnected voids:
$$
n = \frac{V_{void,eff}}{V_{tot}}
$$
For istance clay has voids but they are not interconnected so $n_V > 0$ but $n = 0$. For matrixes like sand or gravel $n_V = n$.

## Compressibility
Praticamente stiamo cercando di dire che se tolgo o meto liquido in una matrix la porosità varia e la presione totale si distribuisce differentemente tra componente idrostatica e meccanica.

## Storage Coefficient
> The equivalent of $c_p$ in heat transfer

Is defined as the variation in water mass in unit volume of porous media due to a variation of $1 \; Pa$.
$$
S_0 = \frac{\rho g \Delta V_f}{V_{tot}\Delta p} \; [1/m]
$$

## Head or Hubbert Potential
> In italian head is *"prevalenza"*
Fluid movement can be described with vector fields but in our study we use a scalar potententail which is more convinent.

> <span style="color:red">**Hp**:</span> Flow in saturated porus medium  
> <span style="color:red">**Hp**:</span> Incompressible flow  
> <span style="color:red">**Hp**:</span> No viscosity effects (Laminar flow)  
> <span style="color:red">**Hp**:</span> Isothermal  
> <span style="color:red">**Hp**:</span> Relative pressure to $p_{atm}$  

The head or hubbert potential is defined as the total work needed to move a fluid, which is the sum of:
- $U$: Potential Energy (variation in height: z)
- $K$: Kinetic Energy (Which we assume negligible)
- $P$: Energy to overcome pressure gradients

$$
\textbf{H}^* = |g|m \Delta z + m \int _{p_0}
^{p_1} \frac{dp}{\rho}
$$

Given that the fluid is incompressible the presure integral becomes $\Delta p$.

Then dividing both sides by $mg$ we obtain the head:
$$
\textbf{H} = \Delta z + \frac{\Delta p}{\rho g} \; \; \;[m]
$$

## Hydraulic Conductiviy
Signifies the ease of passage of water though porous media under the action of a head gradient.  
The following is the empirical definition which comes from the observations of Darcy (following paragraph):
$$
H = - \frac{Q L}{A \Delta \textbf{H}} \; \left[\frac{m}{s}\right]
$$
While the proper definition of $H$ contains information of the matrix $k$ and of the fluid $\mu$ and $\rho$:
Where $H$ is the hydraulic conductivity defined as:
$$
H = \frac{k \rho g}{\mu} \; \left[\frac{m}{s}\right]
$$

## Velocity
### Darcy Law and Darcy Velocity $v_d$
Is an empirical law used to correlate the flowrate to a pressure gradient.

Hypotesis to be added:
> <span style="color:red">**Hp**:</span> Steady State  
> <span style="color:red">**Hp**:</span> Homogenous Medium  
> <span style="color:red">**Hp**:</span> No sources nor sinks  
> <span style="color:red">**Hp**:</span> $H$ is constant in time and space

$$
Q = H \frac{A}{L} \Delta p
$$

We can manipulate this definition to obtain the **apparent velocity of the fluid phase**, usually known as **Darcy velocity** or specific flow rate:
$$
v_d = -H \nabla \textbf{H} [m/s]
$$
> Similarly to Multiphase systems this would be the *fluid only* velocity that is the velocity considering the whole cross section we would have only the fluid.

If the system is heterogenous $H=H(\vec{x})$.  
If the system is also anisotopic then $H$ becomes a tensor $\underline{\underline{H}}$

### Pore Velocity $v_p$
> Again using the similariy with multiphase systems this would be the *fluid alone* condition, that is the velocity of the fluid phase only considering its own cross section.

$$
v_p = \frac{Q}{A_{water}} = \frac{Q}{A \cdot n} = \frac{v_d}{n}
$$

### Microscopic velocity
It can be defined by looking at the real path travelled by a water molecule in the porous matrix.
If we define the *tortuosity* $\tau$ of the flow as the ratio between the real path lenght and the linear one we can then obtain a micorscopic velocity as follows:
$$
v_{micro} = v_p \cdot \tau
$$