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
- Non ne ha indicati altri.

Wall Lubrication:
- Antal et al. - 1991
- Tomiyama et al. - 1995
- Hosokawa et al. - 2002

Virtual Mass: None, not relevant since we get to stable regimes at steady state

Turbolent Dispersion:
- Burns et al. - 2004
- Lopez de Berodano - 2004
  
#### Side-track: Alla ricerca della convergenza
To understand why it is not converging we made animations of volume fracion and air velocity to try and understand what is the simulation doing.  
By doing so we have observed that the simulation look like diverges as soon as the first blob of air tries to detach from the bottom of the cylinder, maybe a boundary layer on the bottom surface could help.  
Same setting as the previous, just replaced the mesh.  
It diverges very badly. (floating point exception after less then 100 iterations)  
Back to the previous solution.


### 03 - Finer Mesh
We reduced minimum cell size from 15mm to 10mm   
We have reduced the boundary layers from 16 to 10