# Transport Equation
We evaluate the transport of water to obtain the velocity of the flow. That is needed to solve the transport of the solute.

## Generic steady state water flow in saturated porous media
First of all a general waterflow in a saturated porous media.  
We combine 2 equations:  
- Darcy law: $v_d = -H \nabla \textbf{H} [m/s]$
- Continutity equation

> <span style="color:red">**Hp**:</span> Steady State 

$$ 
v_d = -H \nabla \textbf{H} \\
\cancel{\frac{d}{dt} n \rho} = - div \left(\rho \vec{v_d} \right)
$$
Which results in the general waterflow equation for saturated porous medium:
$$
\nabla \cdot (\underline{\underline{H}} \nabla \textbf{H}) = 0
$$
If it's homogenous and isotropic it's simply:  
$\nabla ^2 \textbf{H} = 0$


### Derive the continutiy equation
> <span style="color:red">**Hp**:</span> Saturated Porous Media  
> <span style="color:red">**Hp**:</span> No sources nor sinks  
> <span style="color:red">**Hp**:</span> Isothermal conditions

Reference a reference volume and its boundary.
The variaton in time of mass inside the volume is the net balance across its boundary
$$
\frac{d}{dt} \int _\Omega n \rho dV = - \int _{\delta \Omega} \rho v_d \hat{n} dS
$$
Then, as usual apply the divergence theorem to the RHS, then get rid of the integrals.
$$
\frac{d}{dt} n \rho = - div \left(\rho \vec{v_d} \right)
$$

## Generic transient water flow in saturated porous media
From the solution of dacry + continuity transport equation we add the following terms:
- $\rho \Delta V$: mass of incoming or outcoming water (Source/Sink term)
- $\rho S_0 \frac{d\textbf{H}}{dt}$: Storage term (like $\rho c_p \frac{dT}{dt}$) 
So the generic water flow equation is:
$$
\rho \Delta V + \rho S_0 \frac{d\textbf{H}}{dt} = \nabla \cdot \left( \rho \underline{\underline{H}} \nabla \textbf{H} \right)
$$

### In a Confined Acquifer
Starting from the transient soultion so it's more generalized.  
> <span style="color:red">**Hp**:</span> 2D Flow (horizontal)  
> <span style="color:red">**Hp**:</span> $H$ is a scalar that depends on the position: $H(\vec{x})$
We have an impermeable layer above $b_2(x,y)$ and below $b_1(x,y)$, which we assume are planes.  

- We integrate the RHS of the general transient equation between the two planes:
$$
\int _{b_1} ^{b^2}  [...] dz
$$
- We only consider the coordinates $x$ and $y$ (2D flow), 
- Apply the Leibniz theorem.  
- Get rid of flux terms perpendicular to $b_1$ and $b_2$ since they are impermeable (so no flow across them).  
So we are left with:
$$
LHS = \nabla_{x,y} \cdot \int _{b_1} ^{b_2} \left( H(x,y,z) \nabla_{x,y} \textbf{H} \right) dz 
$$
But the only term that depends on $z$ is $H(x,y,z)$  
so we define the **Hydraulic Trasmissivity Coefficient**: $T(x,y) = \int _{b_1} ^{b_2} H(x,y,z)dz$
therefore:
$$
LHS = \nabla_{x,y} \cdot \left( T(x,y) \nabla_{x,y} \textbf{H} \right) dz 
$$
If it's steady state the LHS is simply 0.  
Otherwise we have to apply the integration on the LHS as well:
- Source term: $s(x,y,t)$
- Storage term: $S_0 \cdot B(x,y) \cdot \frac{d\textbf{H}}{dt}$
  
Where $B(x,y)$ is the acquifer thickness.  
We can define $S = S_0 \cdot B(x,y)$ which is the storage coefficient for the whole acquifer.

> In a **phreatic acquifer** the solution is similar but instead of the upper bound we have a free upper bound that can change in time

## Tranport of Solutes: Advection Dispersion Equation (ADE)
For this one we have to model the trasnport of a solute in water by using its concentration $C(t)$ (mass of contaminant over volume of solution). 

### Advection 
Movement of the solute with the waterflow  
$$
\phi _{advection} = C \cdot \vec{v_p}
$$
### Diffusion
The solute can diffuse (molecular diffusion) behind and upfront spreading the concentration  
$$
\phi _{diffusion} = - \underline{\underline{D^*}} \nabla C
$$
where $\underline{\underline{D^*}} = D_{water} \cdot \underline{\underline{T}}$ and $T$ is the tortuosity tensor. Basically we are considering the diffusion of the solute in water plus the effect of the path restriciton.  
### Dispersion
Mechnical dispersion of the particles due to the nature of porous media, is described as the diffusion equation but the nature of the phenomena are different.  
The law is empirically defined similarly to the diffusion law:
$$
\phi = - \underline{\underline{D}} \nabla C
$$
Where $\underline{\underline{D}}$ is the dispersion coefficient:

$$
\underline{\underline{D}} \sim f(\underline{\underline{\underline{\underline{a}}}},\vec{v_p}, Pe, r)
$$
The dispersion coefficient depends on the dispersivity coefficient whihc is a 4th order tensor taking into account the structure tortuosity and orientation of the channels in the porous media, the pore velocity, the peclet number and a dimentionless factor $r$ related to the shape of the channels.  
In a very simplified case of homogeneous and isotropic medium $a$ becomes just 2 components: $a_L$ for longitudinal dispersvity along the flow direction and $a_T$ for transveral dispersitvity normal to the flow direction.  

> Lab scale and field scale show differences in $a_L$, where the first one is always close to thegrain size while on the filed results to be in the order of magnitude of the 1 to 10 meters. Only at the lab scale we find that $a_T \sim \frac{a_L}{10}$.

>**In simple terms...**  
> *Advection* is the simple transport let's call it, informally, "mechanical".  
> *Diffusion* tends to move contaminants in any direction, that what moves contaminants to opposite direction to the flow at the beginning, the "diffusion force" in an isotrpic medium is equal in all direction and is not dependent on the flow direction.  
> *Dispersion* also moves contaminants in any direction but is never isotropic beacuse the direction of the flow does matter.

### Derivation of the Advection Dispersion Equation

> <span style="color:red">**Hp**:</span> Saturated Porous media  
> <span style="color:red">**Hp**:</span> Contamimant has no chemical reaction with the solid matrix

Start with the continutity of mass ($ndS$ is the porous surface):
$$
\frac{d}{dt}\int _\Omega C \cdot (n dV) = - \int _{\delta \Omega} \vec{\phi} \hat{n} (ndS) 
$$
- To the flux term we substitute the sum of the three components
- Apply divergence theorem and remove the integral
- For convienece define a hydrodynamic dispersivity coefficient $\underline{\underline{D_h}}$ as the sum of the coefficients for dispesion and diffusion

$$
\frac{d}{dt}nC = - \vec{v_p}n \nabla C + \nabla \cdot \left(  \underline{\underline{D_h}} n \nabla C \right)
$$

To this equaiton we can add other terms to model other phenomena like:
- Sink and sources $\pm W$
- Chemical reactions between solute or water and the matrix $\pm Ch$
- Decay (Radioactive or biological) $-\lambda C$  

And at last the **Sorption term** $\pm S$ which takes into account the exchange between liquid and solid. 

### Sorption Term
Sorption is the general term for both:
- **adsorption**: exchange at the surface  
- **absorption**: exchange in the bulk

The process can be physical due to electrostatic forces (reversible process) or due to chemical interactions (irreversible). The process is influenced by pH, temperature and concentration of the solute (or other solutes). In our study we simplify to $S=S(C,F_{abs}) [kg/(m^3s)]$ where $F_{abs}$ is the **ratio between mass of solute sorbed to mass of solid** (Is the quantity we plotted during labs 2 and 3).

So we add another equation for the balance of sorption ($\rho F_{abs}$ is a concentration):
$$
\frac{d}{dt} \rho F_{abs} = S(C,F_{abs}) \pm \text{other}
$$
Where our unknown is $S(C,F_{abs})$.  
We use models to describe the sorption process using the **Equilibrium Sorption Isotherms** since they are for a constant temperature. We consider them at equilibrium so at steady state, we assume no transition phases and that a variation in concentration in the liquid causes a sudden change in the concentration in solid.  
The curves are $F_{abs}$ as a function of $C$ at fixed temperature.   
We introduced three types:  
- Linear $F_{abs} = K \cdot C$  
- Freundlich $F_{abs} = K_1 \cdot C ^ {K_2}$  
- Langmuir $F_{abs} = \frac{K_1 \cdot C}{1 + K_2 \cdot C}$  

Freundlich is an empirical power law good for multi-layer systems (no saturation) while the Langmuir is good for single layer systems where saturation can be reached.  

We can then solve the system:
$$

\frac{d}{dt}nC = - \vec{v_p}n \nabla C + \nabla \cdot \left(  \underline{\underline{D_h}} n \nabla C \right) - S \\

\frac{d}{dt} \rho F_{abs} = S(C,F_{abs}) \cancel{\pm \text{other}}

$$
For simplicity once subsituted the model we can rewrite the first equation with a **retardation factor** $R$
$$
R \frac{d}{dt}C = - \vec{v_p} \nabla C + \nabla \cdot \left(  \underline{\underline{D_h}}  \nabla C \right)
$$
That is beacuse due to the sorption processes the transport of the contaminant is slower both in terms of diffusion and dispersion.  

> For low concentration we can just use the linear 

> If we use any but the linear model the breakthough curve will be asymmetrical beacuse the retardation factor will depend on the concentration as well: as concentration lowers the retardation is lager.

> As commented before if we consider unsaturated media we have to use the water content instead of the porosity, which likely depends on the position and time $w(\vec{x},t)$

> if we solve the 1D case for a pulse injection in homogenous medium is the shape of a gaussian.
> if we add the retardation effect changes the velocity $v_p \rightarrow \frac{v_p}{R}$.

## Non equilibrium model
In non equilibrium the rate of adsorption and desorprtion are not equal, therefore we can write:
$$
\rho \cancel{V} \frac{dF_{abs}}{dt} = \dot{D} F_{abs} \rho  \cancel{V} - \dot{A} C n \cancel{V}
$$
Desorption (from solid to solution) rate by the mass of solid minus the adsorption (solution to solid) rate by the mass of solution.  
In steady state the time derivative is zero and the two rates balance out.  
This means that in non equilibrium conditions we have 2 more unkowns. To simplify the problem we can assume that the ratio between adsorptin and desorption at steady state is the same also at non equilibrium conditions.  

$$
\text{Non equilibrium: } \rho \frac{dF_{abs}}{dt} = \dot{D} F_{abs} \rho_{solid} - \dot{A} C n  \\
\text{Equilibrium: } 0 = \dot{D} F_{abs} \rho - \dot{A} C n 
$$
We can substitute an isotherm in the equilibrium case, we assume a linear model for semplicity $F_{abs} = K_1 C$.    
$$
\dot{D} K_1 \cancel{C} \rho = \dot{A} \cancel{C} n
$$
So that we can express one of the rates in terms of the other and substitute in the first one.  
$$
\dot{D} = \frac{\dot{A} n}{K_1 \rho} \\
\rho \frac{dF_{abs}}{dt} = \frac{\dot{A} n}{K_1 \rho} F_{abs} \rho - \dot{A} C n
$$
So that the second equation the only unkown is $\dot{A}$, as $F_{abs}$ can be measured in by kinetics experiments as we did in LAB 3.

## Two Region Model
The two region model is used when we can identify two behaviours in the system:
- Mobile region: where water can flow (the case we have talked until now)  
- Immobile region: water is still, contaminant can move here from the mobile region only by molecular diffusion

Such a configuration can be found in cracked rocks: the main crack allows water to flow but then microscopic cracks on the main crack surface behave as immobile regions.

We are interested in the behaviour of the mobile region to determine contaminant transport, so to model this we simply add a second equation that considers the amount of contaminant that migrates to the immobile region (in 1D):
$$
\frac{dC_m}{dt} = -v_p n_m \frac{dC_m}{dx} + D n_m \frac{d^2C_m}{dx^2} - \alpha (C_m - C_i) \\
\; \\
\frac{dC_i}{dt} = \alpha (C_m - C_i)
$$
Where $\alpha$ is the diffusive exchange coefficient that models the diffusiondue to concentration gradient between the two regions.  
If we want to add sorption to both we simply multiply the LHS by the respective retardation factor $R_m$ and $R_i$.
