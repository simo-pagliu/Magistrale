# Lecture 6 - 29/02/2024
Following **Chapter 3** of the book (Duderstand - Hamilton): 
Comparison for charateristic parameters form the four factor formula between LWR and CANDU reactors,  $K_\infty$ behaviour in a CANDU reator, breeding reactors (convertion or breeding factor)

## Exercise 1
From slide 20 compute a simplified value of K from the neutron "distribution tree" and compute the Convertion Factor, see Notes

## Exercise 2.22 and 3.6
Computation of  $K_\infty$ varing fuel enrichment
The two exercises are basically identical

## Exercise 3.4
Computation of doubling time of fissile material in a fast breeding reactor.
See Notes

## Exercise 3.8 
Computation of $K_\infty$ for an infite homogenus mixture of U-235 and moderator. 
See Notes 
Python script is an attempt to generalize the approach
A possible improvement would follow *Lecture 6 (29/02/2024) Slide 17*
## Exercise 3.9
Re-evaluation of *Reactor Time*, by modifing the initial formulation with the addition of a **Indipendent Source Term**
Python script of a simple resolution with symbolic module.

The solution is the following:


$$N_{t}{\left(t \right)} = \frac{S_{o} l e^{\frac{t \left(k - 1\right)}{l}}}{k - 1} - \frac{S_{o} l}{k - 1}$$

For the analytical approach,
*see notes*