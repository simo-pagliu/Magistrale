# Single Phase Project
The folder structure follows this file.
## 01 - Preprocessing

## 02 - Meshing
### Geometry
The geometry was done in Fusion, it's a cylinder, $50 cm$ in diameter and $2 m$ tall. Exported as a STEP file: `CAD_geometry.step`.  

### Fluent Mesh
#### Model considerations
We relized =that it was smart to understand which model to use beforehand to create the mesh accordingly:
- If we use k-eps the first layer y+ shall be greater then 30 since it cannot solve at the wall  
- If we use low-Re y+ at the first layer should be lower then 1, and then 20 layers    
- If we use k-omega SST the constraint is less strong so we can have a y+ higher then 1  
For multiphase simulation we are going to use eulerial-eulerian approach, the gas phase should be higly diluted so we are going to use the k-omega SST dispersed model.

The mesh is done with multizone meshing  
first layer: 1mm  
16 boundary layers  
growrth rate: 1.2  

surface mesh maximum cell dimention: 15mm

We will verify these choices once the first simulation has been run.  

We computed the velocity to be $0.085~m/s$ given the max cell size of $15~mm$ we got a charateristic time of $0.18~s$. We will use $0.1~s$ as a first time step.  


## 03 - Simulation
### 00 - First Evaluation
We used most of the models from the LAB 12  
For wall conditions the air is set to specified shear stress, 0 Pa to all components as a "free slip" condition.  
Cell zone condition -- Density we left the default option minimum-phse-aveaged  

We initialized with standard, default values (all velocities to 0).  
Having the velocity and the maximum cell size we comuted a charateristic time of 1 ms to use as a reference to choose the time step.

### 01 - Second Evaluation
Transient: Bounded 2 order --> 2 order
Walls: No shear --> No slip for air as well  

We still encounter lack of convergence

#### Models to evaluate
Drag:
- Ishii & Zuber - 1978:  Bubbly flow in different regimes, evaluated separatly
- Grace et al. - 1976:  Formulated for flow past a single bubble, suitable for low volume fractions
- Tomiyama - 1998:  For single bubble in a wide range of proprieties and diameters, focus on bubbles in stangnat liquid
  
(Thanks to the paper of *Yamoah et al - 2015* for the comparison between these models)

It could be worth it to use the Ishii & Zuber model. 

Lift:
- Tomiyama et al. - 2002
- Ziegenhein et al - 2018
- Hessenkemper et al - 2021
Tomiyama paper is the only one hat uses a large channel for their experiment (2m by 2m squared) while the other two studies use thin rectangualr ducts. Also the last two where focused on changes due to impurites in the water.  

Wall Lubrication:
- Antal et al. - 1991
- Tomiyama et al. - 1995
- Hosokawa et al. - 2002
Antal was the first model, modeled with spherical bubbles in stationary water and laminar condition, independent from the pipe geometry.   
Tomiyama expanded Antal to consider the flow field (non still water) and the pipe geometry.  
Hosokawa modifies the Tomiyama to consider a very large lift force that can occur in some flows.

Virtual Mass: None, not relevant since we get to stable regimes at steady state

Turbolent Dispersion:
- Burns et al. - 2004
- Lopez de Berodano - 2004
Burn is a more general "universale" model, the Lopez model can be derived from the Burns one.  
Burns was also tested for bubbly flow in vertical pipe and showed better predictions in all cases. 
The Lopez model was developed for Medium-Sized bubbles in the elipsoidal particle regime.  
We might want to specify the new coeffieent for the Lopez model as found in the paper by Burns et al.
  
#### Side-track: Alla ricerca della convergenza
To understand why it is not converging we made animations of volume fracion and air velocity to try and understand what is the simulation doing.  
By doing so we have observed that the simulation look like diverges as soon as the first blob of air tries to detach from the bottom of the cylinder, maybe a boundary layer on the bottom surface could help.  
Same setting as the previous, just replaced the mesh.  
It diverges very badly. (floating point exception after less then 100 iterations)  
Back to the previous solution.


### 03 - Finer Mesh
We reduced minimum cell size from 15mm to 10mm   
We have reduced the boundary layers from 16 to 10


#### Presence of slugs:
We computed $D_*$ to be 184 $>52$ which means that we cannot have formation of slugs --> We should have an heterogenus flow, so we should consider bubble interactions.  

#### Flow region
From the velocity $0.0085 m/s$ knowing the diameter to be $0.5m$ we should in the heterogenous region

#### Eotnos Number
We computed $Eo=3.13$ for small  
$Eo = 22.6$ for large  
Confirming it's good :D

#### Free slip condition
We set specified shear to 0Pa on all walls for the water phase