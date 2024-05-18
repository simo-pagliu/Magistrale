# Introduction
First lecture was just an introduction to the course, logistics and some data about the nuclear industry.

### Lecture 2 - 21/02/2024
Nuclear reactions, decay law, Decay+source differential equation with analytical solution to the problem
- Exercise 1 explained during lecture, *Lect2_es1.py*
- Exercise 2 for home, *Lect2_es2.py*

### Lecture 3 - 22/02/2024
Focus on nucleus related reactions, cross sections, definition of uncollided flux, macroscopic cross section, auxiliary quantities and probability of exponential distributions  
*Lect2_Decay.py*

#### Exercise 2.6 *Lect3_es2-6.py*
Presented during lecture, left for home. (Last Slide)
Correct, *Rooijen* suggests to, instead of using the total macroscopic cross section $\Sigma _{tot}$, to only consider absorption $\Sigma _{a}$,so that the solution takes into account any neutron that had interactions different from absorpition: a neutron can be scattered but that doesn't mean that it will stop where is was scattered.
The solution remains unchanged with the two approaches.

#### Exercise 2.7 *Lect3_es2-7.py*
Presented during lecture, left for home. (Last Slide)
Correct, Reaction rate for a thin target is give, by definition:
$$R = \sigma_t I N_A$$
The interaction rate of an individual nucleus is given by the same, removing teh atomic density $N_A$ from the expression.

#### Exercise 2.8 *Lect3_es2-8.py*
Presented during lecture, left for home. (Last Slide)
**NOPE** check *Rooijen* page 15

### Lecture 4 - 27/02/2024
Fission, fissile vs fissionable, neutron "journey" inside thermal and fast reactors, prompt and delayed neutrons, average number of neutrons produced, energy spectra of fission neutrons.  
We then worked with Laplace transforms, carolina solved an exercise: *Lect4_es1.py*, I then tried to solve it "my way", starting from differential equations and solving it with python: *Lect4_es1-VAR.py*

# Simple models
Following **Chapter 3** of the book (Duderstand - Hamilton)  
Multiplication factor, four and six factor formulas, reactor time

### Lecture 5 - 28/02/2024
Multiplication factor, neutron lifetime, simple reactor model (Reactor Time) and four factor formula  

#### Example 1 *Lect5_chernobyl*
Invented by the professor, Simplified computation of the power released during chernobyl accident.
The simplified model of the Reactor Time can be used for evaluating accident scenarios

### Lecture 6 - 29/02/2024
Comparison for charateristic parameters form the four factor formula between LWR and CANDU reactors,  $K_\infty$ behaviour in a CANDU reator, breeding reactors (convertion or breeding factor)

#### Exercise 1 
From slide 20, we computed a simplified value of K from teh neutron "distribution tree" and the Converion Factor, *See Notes*

#### Exercise 2.22 and 3.6 *Lect6_es3-6.py*
Computation of  $K_\infty$ varing fuel enrichment
The two exercises are basically identical

#### Exercise 3.4 *See Notes*
Computation of doubling time of fissile material in a fast breeding reactor.

#### Exercise 3.8 *Lect6_es3-8.py*
Computation of $K_\infty$ for an infite homogenus mixture of U-235 and moderator. 
*See Notes*
Python script is an attempt to generalize the approach
A possible improvement would follow *Lecture 6 (29/02/2024) Slide 17*

#### Exercise 3.9 *Lect6_es3-9.py*
Re-evaluation of *Reactor Time*, by modifing the initial formulation with the addition of a **Indipendent Source Term**
Python script of a simple resolution with symbolic module.

The solution is the following:


$$N_{t}{\left(t \right)} = \frac{S_{o} l e^{\frac{t \left(k - 1\right)}{l}}}{k - 1} - \frac{S_{o} l}{k - 1}$$

For the analytical approach,
*See notes*

# Neutron Transport Model
Following **Chapter 4** of the book (Duderstand - Hamilton)

### Lecture 7 - 05/03/2024
Introduction to basic quantities useful for the neutron transport model
 - Requirements of the model
 - Neutron density
 - Reaction rate density
 - Neutron flux (Not a mathematical flux, is a scalar)
 - Current Density (Mathematically correct Flux, is a vector)

All quantities as "normal", in respect to Energy $(E)$, in respect to the solid angle $(\Omega)$ and both $(E, \Omega)$  
At last, Riva proceed with a really in-depth mathematical proof regarding Scattering cross-sections, differential $\sigma _s$, double differential $\sigma _s$


#### Ex. 4.2 *See Notes*
Really simple example to understand how the quantities behave (vector and scalar quantities)

#### Animation *Lect7_Animation.py*
Done by Carolina after the extremly long mathematical show of Riva regarding Scattering Cross Section,  
I'm trying to do it with manin but i have no idea how to compute the second scattering angle and therefore I'm stuck...

### Lecture 8 - 06/03/2024 
Exercises on fundamental quantites

#### Ex. 4.3 *See Notes*
Flux, Current density, Partial Current density

#### Ex. 4.4 *See Notes*
Shperic reactor, *Roijen* solution is slightly different in interpretation then the one given by prof.Cammi

#### Ex. 4.5 *See Notes*
Current Density, spheric coords

### Lecture 9 - 07/03/2024
- The **neutron transport equation**, deduction, gain and loss terms. 
- Side note on *double differential cross-section*
- 1D form of the neutron transport equation 
- Charaterization of the source term

### Lecture 10 - 12/03/2024
Following **Chapter 4 - Sections II and III** of the book (Duderstand - Hamilton):  
Prof. absent, Lecture by Riva and Carolina

- Recap of numerical methods
- Legendre polynomials expansion
- Spherical Armonics expansion
- Discretization of $E$ and $\Omega$
- Approximations (isotropic, one speed, steady state)
- Solution in vacuum

At the end of the Lecture Carolina presented the first Python Homework and a python script for Legendre expansion

### Lecture 11 - 13/03/2024
Following **Chapter 4 - Section IV Subsection A** of the book (Duderstand - Hamilton): 
- Recap of the numerical approach to solve the Boltzmann equation
- Integration of the Boltzmann equation over all directions $\Omega$ to get $\Phi$: "Neutron Continuity Equation"
- Trying to express the equation in terms of $J$

At the end we have created 2 expressions for the boltzmann equation, one in terms of $\Phi$ and the other in terms of $J$, in both cases the equation is not solvable due to the fact that, when integrated, the spatial term gives a new unkown (1 equation, 2 unknowns = unsolvable equation). These two expressions are discretized over the solid angle, which means that they are 2 (vectorial) P1 equations (6 scalar). Next step is to approximate this system of 2 (vect.) equations in 3 unknowns (vectors), the approximated solution will be the diffusion equation.

#### Study Note:
It is worth it to take a good look at section **B** since it recap quite well all the userful approximations used during this and following lecture

### Lecture 12 - 14/03/2024
Following **Chapter 4 - Section IV Subsection C and D** of the book (Duderstand - Hamilton): 
- From the Boltzmann neutron transport equation to the diffusion equation
- Approximations
- Energy Dependant expression (just cited, didn't get into much detail)

Basically all section **C**, presented in a different manner but the result is the same (the book's approach is a bit faster and is sufficient for the exam), section **D** was just cited (existance of the *Energy dependant diffusion equation*).  
We then exposed the points of section **E**, without going into detail, they just explained the diffusion equation limitations: *See Notes*  

#### Study Note:
It is worth it to take a good look at section **B** since it recaps quite well all the userful approximations used during this and previous lecture

#### Ex. *See Notes*
We did, once again, an exercise from an exam regarding net number of neutrons $J$ and tot number of neutrons $\Phi$.  

### Lecture 13 - 19/03/2024
We followed the last part of the Chapter, focusing on the Boundary and Initial conditions for the diffusion equation.  
Basically we started from the transport equation conditions which are correct and mathematical derived, and then we try to "translate" them for the diffusion equation (which is an approximation).  
The result is that the conditions of the diffusion equation is not an exact condition but approximation of those conditions. 

#### Ex. ??? and ??? *See Notes*
Both executed in class, apparently unnamed

#### Ex. 4.11
For Home

#### Python Code
During class Carolina showed us some plots of simple solutions of the diffusion equation

# Diffusion Equation
Following **Chapter 5** of the book (Duderstand - Hamilton)  

### Lecture 14 - 20/03/2024 
Another path to the derivation of the diffusion equation.  
Derivation of notable solutions:
 - Planar Source
 - Point Source
 - Slab Geometry

### Lecture 15 - 21/03/2024
Just exercises from previous exams regarding solving the diffusion equation with notable cases, *See Notes*.

### Lecture 16 - 26/03/2024
Professor Cammi went through the solutions of the diffusion problem solved by Riva and added:
 - Line Source
 - Verification of the solution (Source term should equal the number of absorption and leakages)
 - Introduction to Neutron reflection

### Lecture 17 - 27/03/2024
 - Reflectors
 - Albedo as Boundary Condition (example of infinite slab with a planar source)
 - General diffusion problems
 - Green's Functions for linear system

 
### Lecture 18 - 28/03/2024
 - Eigenfunction expantion methods *Book Page 171*
 - General solution for a time dependent slab reactor with the eigenvalue expansion method
 - Observation regarding *long time behaviour* of the previous solution
 - Observation regarding *criticality* of the previous solution

### Lecture 19 - 3/04/2024
 - Solution assuming separation of variables *Book Page 203*
 - Conncection of diffution solution with the 4 (and 6) factors formula
 - Physical meanings of the terms
 - Approach for more general geometries --> Condition on reactor power to get the complete solution
 The professor then proceed with several examples, I wrote on my notes the solution for a sphere,  
 the one that is present in the book it's only the last one: finite cylinder *Book Page 208*.  
 In the book a table with notable solution can be found at *Book Page 209 table 5-1*.
 He ended the lecture stating that this approach shows problems if you want to consider reflectors.

### Lecture 20 - 04/04/2024
We did some exercises regarding the criticality condition of a reactor

#### Python Exercise
- Compute the critical core volume 
- Neutron leakage fraction from the critical core 
- Neutron lifetime

#### By hand Exercise
Criticality Condition of a box reactor. Find the critical condition.  
Second request was to minimize the volume (Riva showed us 2 possible ways to solve this).  
*See Notes*

### Lecture 21 - 10/04/2024
(*We didn't had lecture on 9/04*)  
We solved the problem of slab reactor with infinite reflectors, with an example of solution, *See Notes*

# Mathematical Methods for Nuclear Reactor Dynamics

### Lecture 22 - 11/04/2024
He started a series of lectures about mathematical methods used to solve nuclear reactor dynamics problems,  
first of all was the Laplace Transform

### Lecture 23 - 16/04/2024
Linear system theory

### Lecture 24 - 17/04/2024
Continuation on linear system theory with an example

### Lecture 25 - 18/04/2024
Stability of numerical models with system theory  
Transfer function Analysis (Fazzi style) with an example

# Nuclear Reactor Kinetics
Following **Chapter 6** of the book (Duderstand - Hamilton)  

### Lecture 26 - 23/04/2024
- How to consider precursors and delayed neutrons, groups approach  
- General solution for just one group: point reaction kinetics   
- Mean Generation time, reactivity  
- Addition of an external source term for startup  

### Lecture 27 - 24/04/2024
- One group kinetics Equation gives infinite solutions, to solve this you have to set initial conditions on $P$ power, $C$ precursors rate and their derivatives in respect to time $\frac{\delta}{\delta t}$  
- Quadratic formula gives $s_1$ and $s_2$   
- Approximate expressions for $s_1$ and $s_2$  
- Observation of fast and slow transients  
- General solution at startup (external source)
- How to express power with the group approach



## Userful stuff to take a look:
signal library on python (userful to study stability of system and linear systems)  
in-hour equation: https://en.wikipedia.org/wiki/Inhour_equation  