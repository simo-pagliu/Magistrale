# Single Phase Project
The folder structure follows this file.
## 01 - Preprocessing
Average temperature = 322.99K

## 02 - Meshing
### Geometry
The geometry was done in Fusion, it's the model of **Bali-2**: 
- a quarter of a circle
- $2 \, m$ in radius 
- $+z$ is the axis, $+x$ is the radius
- extruded to a depth of $15 \, cm$ as the real model

Exported as a STEP file: `CAD_geometry.step`.  

### Fluent Mesh
The system is in natural convection, the flow will be highly anisotpic, therfore we cannot use standard k-eps or k-omega nor low-Re models.  

The case is in turbolent flow since $Ra >> 10^{9}$.  

So we can use:
- SST + "corner correction" = quadratic correction (y+ is not required to be <1 but the grid should be able to catch all the microstructures of the flow, so we still need it around 1)

- `Waterthight Geometry`
- No `local sizing`
- Surface mesh $Min = 1 mm$ and $Max = 50mm$  
- `Only fluid with no voids`
- Boundary layer: $20$ layers, first height: $1.25$, growth rate: $1.2$
- Multizone meshing: `hex-pave`
-


## 03 - Simulation
### 00 - First Evaluation
We activated gravity, energy model, transient simulation, standard initialization at 300K no velocity.  

Water as fluid with given data, density was set to Boussinesq approximation since we need to simulate natural convection.  

We set the front and back surfaces to periodic conditions.  
We set the Temperature to 273.15K on the curved wall.  

We then set the power generation by adding a source term in the fluid cell conditions, from the given power over the volume we get the power density of $P = 31.8 \frac{kW}{m^3}$. We also checked the power by inverting the given Rayligh correlation and we got a coherent result $P = 31.4 \frac{kW}{m^3}$.  

To set up the simulation we compute the time step as  $\tau = \frac{L}{\sqrt{g \beta L \Delta T }} = 5.3s \rightarrow \Delta t = \frac{\tau}{n} = 0.53$, we used $\Delta T = 35$ which we derived from the plot of the experimental data, and $n = 10$ from a previous experience. We might refine this values later.

For models we used the $k-\omega \, SST$ because is the best, production limiter OFF and we activated *Corner FLow Correction* to keep in mind the 90 degree angles of the geometry.

Whitin this run we plan to verify:
- y+ at the wall (countour)
- max and avg (should be $Co \sim 1$) Courant Number (reports definitions)

From this first run we have determined that the mesh is too coarse from:
- velocity profile --> shows large variation between cells
- y+ @wall --> larger then 1 at curved wall
Also this has been confirmed by the fact that the $Co$ is much lower then 1.

### 01 - Refined Mesh


