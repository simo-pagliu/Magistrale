## Discretization 1
We implemented the central differences scheme for the diffusion problem (heat diffusion)

## Discretization 2
Central differences scheme for diffusion + advection (= convetion)
If Peclet number is > 0.1 (too high) the solution becomes unstable beacuse we have no info on the direction of the flow (if Pe is high --> the flow is not negligible)  
To see the effect just change the velocity $u$ to something grater

## Discretizaton 3
We use the 1st order upwind which is always stable BUT it is un-physical beacuse you create "false diffusion" when the flow direction is not aligned with the grid --> the result will be different from the real solution  
EVIDENCE: For a pure convetive problem we see some diffusion  
SOLUTION: Use second order upwind  

(Prof. noted that we can use the 1st order to start the computation (it's stable and faster), then switch to second order for actual result)