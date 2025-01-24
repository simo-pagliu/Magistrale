# Notes on exercises

## Uranium mining
THere are price categories of uranium, usually:
- < 80 $/kgU
- < 130 $/kgU
- < 260 $/kgU  
  
The first one is the most interesting as it can be extracted at low cost, most of this uranium is in Kazakistan.  
The second cat. is less convienent but can still be a viable option in some situation (think about the greater picture)  
The last option is most likely never, not even close, economically viable.

Recovery cost:
$$
RecoveryCost = \frac{MiningCost}{Grade \cdot RecoveryRate}
$$
Where grade is a measurment of the purity of the ore
$$
Grade = \frac{m_{U3O8}}{m_{ORE}}
$$

## Enrichment
SWU: Separative work unit, indicates the energy needed to enrich and therfore the cost of the enrichment process, sometime used the SWU Factor $SF = \frac{SWU}{Prod}~[SWU/kgU]$  

$$
SWU = \dot{P} V(x_p) + \dot{W} V(x_w) - \dot{F} V(x_f)
$$

where, $\dot{I}$ are usually mass flow rates, but can also be mass or volume  
$V(i)$ is the  separation potential:  
$V(i) = (2 x_i -1)ln\left(\frac{x_i}{1-x_i}\right)$

P stands for Production (Enriched, Output)  
W stands for Waste (Depleted stream or Tails)  
F stands for Feed (Natural, Input)  

$R_i$: Relative isotopic abundance
$$
R_i = \frac{x_i}{1-x_i}
$$
Where $x_i$ is the enrichment of the stream $i$.  
We compute $R_P$, $R_W$ and $R_F$.

$\alpha$: Stage separation factor = $\frac{R_P}{R_W}$  
$\beta$: Heads separation factor = $\frac{R_P}{R_F}$  
$\gamma$: Tails separation factor = $\frac{R_T}{R_F} \equiv \frac{\beta}{\alpha}$  

$N_e$: Number of enriching stages
$$
N_e = ln \left( \frac{R_P}{R_F} \right) \frac{1}{ln(\beta)}
$$

$N_s$: Number of stripping stages
$$
N_s = ln \left( \frac{R_F}{R_T} \right) \frac{1}{ln(\beta)} - 1
$$

**Notice that the first ratio in the first logarithm is computed in respect to the whole process: initial feed, final product and final waste values While the $\beta$ to the single stage.**

  


Total number of stages needed is $N = N_e + N_s$

In an idial cascade $\alpha = \beta ^2$ and $\beta = \frac{1}{\gamma}$

If enrichment is increased:
- we reduce spent fuel
- we increase depleted waste
- waste from mining and milling is costant
  
If we improve the enrichment process by reducing the waste enrichment:
- we reduce depleted waste
- we reduce mining and milling waste
- spent fuel is costant

Reflux ratio for the $n^{th}$ stage:
$$
rr = \frac{W_n}{F_n}
$$

For a gas centrifuge the max velocity is determined by:
$$
\sqrt{\frac{\sigma_s}{\rho}} = v_a = \omega a
$$
where a is the radius at the outer wall.

## Economics

Cost of electricity is given by:
Capital + O&M + Fuel  
To this you have to consider the uptime and the grid demand:  
Operation = UPTIME * Power * CF * Cost of primary energy source  
Maintainance = Grid Demand Power * CF * Cost of replacement energy source  
Demand = UPTIME * (Grid Demand Power - Power * CF ) * Cost of replacement energy source  

This is beacuse we always ahve to satisfy the grid demand for energy and it is possible that while up we have to integrate the production with a secondary energy source.  
Overall the tred make it such that: $CF \uparrow \rightarrow Cost \downarrow$

## Out of core managment

T: Length of the Refuleling cycle  
E: Energy produced in a cycle = $CF \cdot P_{th} \cdot T$  
$Bu_c$: Cycle Burnup = $\frac{E}{m_{core}}$  
$Bu_d$: Discharge Burnup (Admissible of the fuel/technology)   
$N_r$: Number of core regions which corresponds to the number of cycles within a refuling cycle = $\frac{Bu_d}{Bu_c}$  

The number of regions has to be rounded up: $2.7 \rightarrow 3$, in this case we will have 3 regions:  
- all of them have 1 batch to be burned 2 times.   
- 2 of them will have another batch to be burned 3 times.

Then you get the Number of assemblies in a region $\frac{Assemblies}{N_r(\text{not round up})}$, then round it up.  
The 2 regions with full batches will be full,  
the last region with 1 batch only has to be filled with the remaning assemblies.

in a 560 assemblies core, 3 regions, two filled: $560/2.7 = 207.4 \rightarrow 208$ Assemblies per region:
- Region 1: 208
- Region 2: 208
- Region 3: $560 - 2 \cdot 208 = 144$
  
All the the batches that have to burn only 2 times (as region 3) will have 144 assemblies, so:

- Region 1, Batch a: 144
- Region 1, Batch b: 64
- Region 2, Batch a: 144
- Region 2, Batch b: 64
- Region 3, Batch a: 144

At last verify the core symmetry condition, if the core has "quarter core symmetry" then **all the batch numbers** and the $N_r$ have to be divisibile by **4**.  
(If three-core $\rightarrow /3$, If two-core $\rightarrow /2$, etc..  )

$$
Bu_c = \frac{2}{N_r + 1} Bu_1
$$
Where $Bu_1$ is the burnup of the core if it was just one big region.

## In core managment

Peaking factors

$f_q$: Heat flux factor, it limits the fuel melting, is of interest for the LOCA scenario = $\frac{q'_{MAX}(Pellet)}{q'_{AVG}\%P}$  
Where $q'_{AVG}(Pellet)$ is the max heat flux among the **pellets**  
$q'_{AVG}$ is the average heat flux in the core   
$\% P$ is the percentage of power over the maximum power (if we operate at lower powers we can relax the limits)  


$f_{\Delta h}$: Hentalpy rise factor, it is a limit on the CFH, used  for evaluating the DNB scenario  = $\frac{q'_{MAX}(Rod)}{q'_{AVG}\%P}$  
Where $q'_{AVG}(Rod)$ is the max heat flux among the **rods**

## Toxicity Index
The lower, the more toxic the substance is: is a concentration.  
It express how much does the substance has to be diluted (in air or water) to not pose a danger.  

$$
TI = \frac{A}{V}
$$
Where $A$ is, for radioactive substances, the activity [Ci or Bq]  
$V$ is the **Volume needed to dilute it down to non dangerous levels**

## Decay Heat
$$
Q_{decay}(t,T) = \frac{P_{th}}{E_f}(F(t,\infty) - F(t+T, \infty)) \\

F(t,T) = \sum \alpha _i e ^{-t \lambda _i} \quad \text{(in the US standard)}
$$
where:  
$t$: time after shutdown  
$T$: Operation time

## Separation Factor
Same as deontamination fator, is called separation when tralking about reprocessing to have an idea of the extaction eficiency:
$$
SF = \frac{\left(\frac{Impuirty}{Tot}\right)_{IN}}{\left(\frac{Impuirty}{Tot}\right)_{OUT}}
$$
