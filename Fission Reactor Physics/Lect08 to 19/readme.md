# Lecture 8 - 06/03/2024
Following **Chapter 4** of the book (Duderstand - Hamilton): 
Exercises on fundamental quantites

## Ex. 4.3
Flux, Current density, Partial Current density

## Ex. 4.4
Shperic reactor, *Roijen* solution is slightly different in interpretation then the one given by prof.Cammi

## Ex. 4.5
Current Density, spheric coords
*See Notes*

# Lecture 9 - 07/03/2024
Following **Chapter 4** of the book (Duderstand - Hamilton): 

- The **neutron transport equation**, deduction, gain and loss terms. 
- Side note on *double differential cross-section*
- 1D form of the neutron transport equation 
- Charaterization of the source term

No exercises were performed.

# Lecture 10 - 12/03/2024
Following **Chapter 4 - Sections II and III** of the book (Duderstand - Hamilton):  
Prof. absent, Lecture by Riva and Carolina

- Recap of numerical methods
- Legendre polynomials expansion
- Spherical Armonics expansion
- Discretization of $E$ and $\Omega$
- Approximations (isotropic, one speed, steady state)
- Solution in vacuum

At the end of the Lecture Carolina presented the first Python Homework

## Ex.
No exercises were performed  
Carolina showed us a python script for Legendre expansion

# Lecture 11 - 13/03/2024
Following **Chapter 4 - Section IV Subsection A** of the book (Duderstand - Hamilton): 
- Recap of the numerical approach to solve the Boltzmann equation
- Integration of the Boltzmann equation over all directions $\Omega$ to get $\Phi$: "Neutron Continuity Equation"
- Trying to express the equation in terms of $J$

At the end we have created 2 expressions for the boltzmann equation, one in terms of $\Phi$ and the other in terms of $J$, in both cases the equation is not solvable due to the fact that, when integrated, the spatial term gives a new unkown (1 equation, 2 unknowns = unsolvable equation). These two expressions are discretized over the solid angle, which means that they are 2 (vectorial) P1 equations (6 scalar). Next step is to approximate this system of 2 (vect.) equations in 3 unknowns (vectors), the approximated solution will be the diffusion equation.

## Study Note:
It is worth it to take a good look at section **B** since it recap quite well all the userful approximations used during this and following lecture

## Ex.
No exercises were performed

# Lecture 12 - 14/03/2024
Following **Chapter 4 - Section IV Subsection C and D** of the book (Duderstand - Hamilton): 
- From the Boltzmann neutron transport equation to the diffusion equation
- Approximations
- Energy Dependant expression (just cited, didn't get into much detail)

Basically all section **C**, presented in a different manner but the result is the same (the book's approach is a bit faster and is sufficient for the exam), section **D** was just cited (existance of the *Energy dependant diffusion equation*).  
We then exposed the points of section **E**, without going into detail, they just explained the diffusion equation limitations: *See Notes*  

## Study Note:
It is worth it to take a good look at section **B** since it recaps quite well all the userful approximations used during this and previous lecture

## Ex.
We did, once again, an exercise from an exam regarding net number of neutrons $J$ and tot number of neutrons $\Phi$.  
*See Notes*

# Lecture 13 - 19/03/2024
Following **Chapter 4** of the book (Duderstand - Hamilton): 

We followed the last part of the Chapter, focusing on the Boundary and Initial conditions for the diffusion equation.  
Basically we started from the transport equation conditions which are correct and mathematical derived, and then we try to "translate" them for the diffusion equation (which is an approximation).  
The result is that the conditions of the diffusion equation is not an exact condition but approximation of those conditions. 

## Ex. ???
Executed in class, *See Notes*

## Ex. ???
Executed in class, *See Notes*

## Ex. 4.11
For Home

## Python Code
During class Carolina showed us some plots of simple solutions of the diffusion equation

# Lecture 14 - 20/03/2024
Following **Chapter 5** of the book (Duderstand - Hamilton):   
Another path to the derivation of the diffusion equation.  
Derivation of notable solutions:
 - Planar Source
 - Point Source
 - Slab Geometry

# Lecture 15 - 21/03/2024
Just exercises from previous exams  
Regarding solving the diffusion equation with notable cases, *See Notes*.

# Lecture 16 - 26/03/2024
Following **Chapter 5** of the book (Duderstand - Hamilton):   
Professor Cammi went through the solutions of the diffusion problem solved by Riva and added:
 - Line Source
 - Verification of the solution (Source term should equal the number of absorption and leakages)
 - Introduction to Neutron reflection

# Lecture 17 - 27/03/2024
Following **Chapter 5** of the book (Duderstand - Hamilton):   
Topics:
 - Reflectors
 - Albedo as Boundary Condition (example of infinite slab with a planar source)
 - General diffusion problems
 - Green's Functions for linear system

# Lecture 18 - 28/03/2024
Following **Chapter 5** of the book (Duderstand - Hamilton):   
Topics:
 - Eigenfunction expantion methods (p.171)
 - General solution for a time dependent slab reactor with the eigenvalue expansion method
 - Observation regarding *long time behaviour* of the previous solution
 - Observation regarding *criticality* of the previous solution

# Lecture 19 - 3/04/2024
Following **Chapter 5** of the book (Duderstand - Hamilton):   
Topics:
 - Solution assuming separation of variables (p.203)
 - Conncection of diffution solution with the 4 (6) factors formula
 - Physical meanings of the terms
 - Approach for more general geometries --> Condition on *reactor power* to get the complete solution
 The professor then proceed with several examples, I wrote on my notes the solution for a sphere,  
 the one that is present in the book it's only the last one: *finite cylinder* (book: p.208).  
 In the book a table with notable solution can be found at page 209 (table 5-1).
 He ended the lecture stating that this approach shows problems if you want to consider reflectors.
