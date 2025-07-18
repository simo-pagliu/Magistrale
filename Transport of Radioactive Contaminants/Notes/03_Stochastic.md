# Stochastic Models
## Basics
### Probability Generating Function
The probability generating fucnion is a tool that we are going to usein this derivation.  
We have a system that could assume several states, these are stored in a vector $\underline{a}$.   
The system at any given time could be in a state $a_i$ with its probability $\mathbb{P}_i$.  
The PGF (Probability generating function) uses a dummy variable $\underline{x}$ as proxy to convey the possible states of the system:  
$$
PGF = \sum _i \mathbb{P}_i \left( x_i \right) \ {a_i}
$$
The elements $i$ could rapresent states, types of particle or, in our case, discrete sections of the space domain.

### Objective of the Kolmogorov Approach
We want to solve the trasnpot problem in a numerical way using a discretized approach:
- discretize time $\rightarrow$ time-steps $dt$ with finite differences schemes
- discretize space $\rightarrow$ cells $dx$  
  
For each cell we want to have an average value in the cell $dx$ and we want to observe its evolution in time

### Hypotesis to the Kolmogorov Approach
> <span style="color:red">**Hp**:</span> **$dt$ small enough**: at every time-step only one event can happen  
> <span style="color:red">**Hp**:</span> **time independent**: Markovian Process, every transition is independent from the previous ones  
> <span style="color:red">**Hp**:</span> **space independent**: Linear Process, every transition is independent on what occurs in other cells  
> <span style="color:red">**Hp**:</span> **time homogenous**: The absolute time of occurence does not matter: $t_1, t_2 \; \rightarrow \; \Delta t$  

## Overview of the derivation
### 1. Chapmann-Kolmogorov Identity (CKI)
The CKI describes the probability of evolution of a system from state $i$ to state $f$ taking into account all possible intermediate states $b$ that could occur between the two.  
This is defined in the domain of probability $\mathbb{P}$, we redifine it to the domain of PGF.  
The CKI in the PGF domain depends on the starting $t_1$ and finishing $t_2$ time steps.
### 2. Forward Kolmogorov Equation (FKE)
By deriving the CKI(PGF) by $t_2$ we obtain the general FKE, then we apply the time homogeous hp to get rid of the two time step and only use $\Delta t$.
### 3. Apply to the transport problem
Instead of a generic information $a$ we want to know:
- $\underline{S}$: Number of solutons in each cell
- $\underline{\underline{T}}$: Number of trappons in each cell, for each type of trappon (Trapped by electrostatic forces, trapped by chemical bonds...)

To do so we define two dummy variables $\underline{x}$ to relate to solutons and $\underline{\underline{y}}$ to be related to trappons.
$$
    \text{PGF}: \frac{\partial F}{\partial t} = \sum _z \left( \mathbb{P}_z \frac{\partial F}{\partial x_z} \right) + \sum _z \left( \sum _i \left( \mathbb{P}_z \frac{\partial F}{\partial y_{z,i}} \right) \right)
$$

> **NOTE**: from now on, $z$ indicates the cells (space discretization), while $i$ inidcates the types of trappons
### 4. Obtain average values
By taking advantage of PGF proprieties, the derivative of the PGF by the dummy variable of the a zone $\tilde{z}$ and then evaluate by the unitary vector fro all dummy variables, we get the average value for that zone $\tilde{z}$.=, knowing the initial state at $t=0$: (\underline{a_0}, 0). 

$$
\left. \frac{\partial F}{\partial x_{\tilde{z}}} \right| _{\underline{x} = \underline{y} = \underline{1}} = S(\tilde{z},t|\underline{t_0}, 0)
$$

Same goes for trappons where we have to derive for a cell and a type of trappon $\partial y_{\tilde{i}, \tilde{z}}$.

### 5. Results: the Kolmogorov Equaiton (KE)
$$ 
\frac{\partial dS_z}{\partial dt} = \left(- \sum_i \dot{A}_z (i) - \sum_{z'} \dot{m}_{z \rightarrow z'} - \lambda \right) \cdot S_z + \sum _i \dot{D}_z(i)T_z(i) + \sum _{z'} \left( \dot{m}_{z' \rightarrow z}S_{z'}\right) \\
\; \\
\frac{\partial dT_z}{\partial dt} = \dot{A}_z(i)S_z - \dot{D}_z(i)T_z(i) - \lambda T_z(i) \;\;\;\;
\forall i 
$$

>*To explain it in words*:  
The time variation of solutons in cell $z$ is given by those lost to trapping in that cell $z$ to all possible mechanism $\sum _i$ of absorption $\dot{A}$, to those that migrate $\dot{m}$ to any other cell $\sum _z'$ and those lost to radioactive decay $\lambda$.   
Positive contributions are given by desoption $\dot{D}$ of all possible types of trappons $\sum _i$, and by those that migrate to the cell from any other cell $\sum _z'$.  
Similarly goes for trappons $T$ but here we have one equation for each type $i$.


## 1D Example
We have seen a simple approach to the 1D case:  
> <span style="color:red">**Hp**:</span> Particles can only move to adjecent cells      

To simplify we are going to consider only one type of trappons so we are going to drop the $i$ entirly.

$$
\frac{\partial dS_z}{\partial dt} = \left(- \dot{A}_z - \dot{m}_{z \rightarrow z+1} - \dot{m}_{z \rightarrow z-1}- \lambda \right) \cdot S_z +  \dot{D}_zT_z +  \dot{m}_{z+1 \rightarrow z} S_{z+1}+ \dot{m}_{z-1 \rightarrow z} S_{z-1} \\
\; \\
\frac{\partial dT_z}{\partial dt} = \dot{A}_zS_z - \dot{D}_zT_z - \lambda T_z 
$$


We define the foreward migration rate: $\dot{f} = \dot{m}_{z \rightarrow z+1} = \dot{m}_{z-1 \rightarrow z}$.  
And the backward migration rate: $\dot{b} = \dot{m}_{z \rightarrow z-1} = \dot{m}_{z+1 \rightarrow z}$.  

$$
\frac{\partial dS_z}{\partial dt} = \left(- \dot{A}_z - \dot{f} - \dot{b}- \lambda \right) \cdot S_z +  \dot{D}_zT_z +  \dot{b} S_{z+1}+ \dot{f} S_{z-1} \\

$$

### How to dermine the parameters:  
The unkown are $S$ and $T$ to be solved in each cells, the time derivative can be approached numerically with central differencing schemes.  

The parameters that we have to dermine experimentally are:
- $\lambda$: Decay constant $\rightarrow$ with radiation measurments.
- $\dot{A}, \dot{D}$: Absorption and desoprtion rates $\rightarrow$ with batch and kinetics experiments  (see labs 2 and 3)
- $\dot{f}, \dot{b}$: Forward and Barckward migration rates $\rightarrow$ Correspondence with ADE and data from column transport experiment (see lab 1)

#### How to determine $\dot{f}, \dot{b}$
We take the ADE and correlate its $nC$ with the $S$ from the Kolmogorov equation.  Basically we apply the same discretization approach to the ADE by dividing the 1D domain in cells and applying central differences schemes: $\frac{d(nC)}{dx} = \frac{C_{z+1}-C_{z-1}}{\Delta x}$.  
Then if we compare the discretized ADE and the KE (with all rates but the migration ones set to zero)
$$
\frac{\partial d(nC_z)}{\partial dt} = C_{z+1} \left(\frac{D}{\Delta x^2} - \frac{v_p}{2\Delta x}\right) + C_{z-1} \left(\frac{D}{\Delta x^2} + \frac{v_p}{2\Delta x}\right) - C_{z} \left(\frac{2D}{\Delta x^2}\right)\\
\; \\
\frac{\partial dS_z}{\partial dt} = -\left(\dot{f} + \dot{b} \right) \cdot S_z +  \dot{b} S_{z+1}+ \dot{f} S_{z-1}
$$
So we by analogy:
$$
\dot{f} = \left(\frac{D}{\Delta x^2} + \frac{v_p}{2\Delta x}\right) \\
\; \\
\dot{b} = \left(\frac{D}{\Delta x^2} - \frac{v_p}{2\Delta x}\right) \\
$$

Where the hydraulic dispersivity $D$ and the pore velocity $v_p$ can be determined by means of experiments, see LAB 1.

> **NOTE** These migration rates actually depend on the discretization itself since they depend on the cell size: $\Delta x$!