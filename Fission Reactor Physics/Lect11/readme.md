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