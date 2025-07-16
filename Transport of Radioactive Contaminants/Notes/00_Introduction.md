# Transport of Radioactive Contaminants
**INDEX**
-
-
-
-
-

---

## Introduction
> Very fast recap of the introductory concepts for this course since they are already known.

### Radioactive Waste and Repositories
Decommissioning of nuclear sites produces **radioactive waste**, which must be **characterized** (what it is made of) and **classified** (assigning a level) to ensure proper disposal.
We then reviewed the different types of repositories and their objectives:
- Isolation from the biosphere
- Isolation from human activities
- Possibility of retrieval to treat the waste in the future
- Multibarrier systems: engineered + natural

The main point of interest is that when a repository is built, we must consider how contaminants might escape following a leak. For example, geological disposals might be constructed in crystalline (Olkiluoto - Finland), clay (Andra - France), or salt-based structures, since all are natural barriers to underground water movement.

### Modelling
In modelling contaminant release, we consider three points of reference:
- Source term: What contaminant is leaking (inventory and solubility of radionuclides)
- Near Field: Migration through engineered barriers, can be quite detailed
- Far Field: Migration in the biosphere, very large areas are considered

Near field effects are what we studied in *Radioprotezione avanzata*: corrosion of a drum due to contact with water, mechanical stresses causing cracks in containment, thermal stresses, biodegradation of organic waste, etc.

Far field is the focus of this course: transport of contaminants in the biosphere mostly occurs via waterways through these physical phenomena:
- Advection - Dispersion in porous media
- Molecular Diffusion
- Solid-Liquid Interchange (Solubility/Sorption)
- Chemical Interactions (Redox or Gas Production)

**Why?** Because containment is not forever; we must acknowledge that it will fail sooner or later and determine how much will escape $\rightarrow$ We must ensure no damage to the biosphere nor the population.

Possible objectives of a study on radioactive contaminants:
- Ensure quality of drinking water (design and prevention, evaluate performance of a disposal site)
- Decide where to position monitoring wells (design of the monitoring system)
- Remediation of polluted sites 

### Aquifers
> This part is "new" but really elementary  

**An aquifer contains water that can move.** They can be:
- Superficial or **Phreatic**: easier to contaminate but also to remediate, limited below by an impermeable layer and with a free surface above
- Deep or **Confined**: difficult to contaminate and to remediate, limited above and below by impermeable layers, under pressure
  
We also have aquitard (slower moving aquifer), aquiclude (water cannot move, like in clay), aquifuge (absence of water and it cannot move, like in granite).

Artesian wells are vertical openings to an aquifer; an artesian spring is when water escapes from the aquifer due to a fault in the impermeable layer.

### Porus Media
Some definitions:
- **Porus Medium** is when space is occupied by more then 1 phase, one of which is fluid
- **Solid matrix** is the solid part of the porus medium
- **Void space** is the space not occupied by the solid
- **Dead space** are non connected voids
- **Effective space** are connected voids
  
A porous medium can be saturated if only water is present, unsaturated when both water and air (+ vapour) are present. The unsaturated zone is usually a "transition" region between the terrain surface and the saturated freatic acquifer. In the unsaturated zone we can define the water content $w\% = \frac{V_{water}}{V_{tot}} < n$ and the degree of saturation $n\% = \frac{V_{water}}{V_{void}} \in [0,1]$

> <span style="color:red">**Hp**:</span> Since the main flow of an aquifer is horizontal, we will always assume that we can consider ONLY THE HORIZONTAL FLOW. Therefore: 3D $\rightarrow$ 2D problem.

Porosity depends on:
- **Grain dimensions**
- **Degree of consolidation**: Unconsolidated are gravel, sand or clay, Consolidated are Rocks
- **Assortiment** or Granulometry Distribution: grains of same dimensions $\rightarrow$ well-sorted, otherwise poor-sorted

### Computer models
> This part was done towards the end of the course but is so insignificant that I'm just going to spend a few words here.

We have seen some code implementations of the models seen in class.
We can solve analytically the ADE as shown by the professor in a MATLAB script, I then wrote a quick Python code that solves it numerically (see `github.com\simo-pagliu\COTRA`), these approach
are fine to solve the 1D problem and visualize it but they are not practical to solve real world problems.
For this reason we have seen some model:
- Groundwater Vistas: solves the ADE numerically in 3D, the user can choose between several methods
- RESRAD: similar, but it adds exposure pathways analysis and dose assessment
- Kolmogorov-Dmitriev Models: stochastic models

> Side-note: `COTRA` uses Radau method when the Source term is active and Runge-Kutta 45 when it is not. That is beacuse when we activate a source in the shape of a step function, the ADE becomes a **stiff problem**. RK45 is an explicit method therefore not suitable for stiff problems, Radau is an implicit variation of RK that is "A-stable" therefore able to solve stiff problems (but is also quite slow)