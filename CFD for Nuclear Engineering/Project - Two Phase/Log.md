## Meshing
If we use k-eps the first layer y+ shall be greater then 30 since it cannot solve at the wall  
If we use low-Re y+ at the first layer should be lower then 1, and then 20 layers    
If we use k-omega SST the constraint is less strong so we can have a y+ higher then 1  
For multiphase simulation we are going to use eulerial-eulerian approach, the gas phase is higly diluted so we are going to use the k-omega SST dispersed model.

The mesh is done with multizone meshing  
first layer: 1mm  
16 boundary layers  
growrth rate: 1.2  

surface mesh maximum cell dimention: 15mm

We will verify these choices once the first simulation has been run.


## Simulation
We used the models from the LAB 12  
For wall conditions the air is set to specified shear stress, 0 Pa to all components as a "free slip" condition.  
Cell zone condition -- Density we left the default option minimum-phse-aveaged  

We initialized the air velocity to the computed 13 m/s, STILL SET TO ZERO, WHO CARES.  
All the other velocity are 0  
Having the velocity and the maximum cell size we comuted a charateristic time of 1 ms to use for the time step

Transient: Bounded 2 order --> 2 order
Walls: No shear --> No slip for air as well


MODEL TO TRY:

Drag:
- Ishii & Zuber - 1978
- Grace et al. - 1976
- Tomiyama - 1998

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

