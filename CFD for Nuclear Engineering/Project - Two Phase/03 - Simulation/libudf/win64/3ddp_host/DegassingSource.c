/**************************************************************
UDF for implementing the degassing boundary condition for 2 
dispersed phases
***************************************************************/
#include "udf.h"
#include "sg.h"
#include "sg_mphase.h"
#include "flow.h"
#include "mem.h"
#include "metric.h"

DEFINE_SOURCE(degassing_source_small, cell, thread, dS, eqn)
{
  real source;
  /*tm is referred to the mixture phase*/
  /*ts is is referred to the air-small phase*/
  /*tl is refferd to the air-large phase */
  
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source =  -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP ;
  C_UDMI(cell,tm,0) = source;
  dS[eqn] =  -C_R(cell,ts)/CURRENT_TIMESTEP;
  return source;
}

DEFINE_SOURCE(degassing_source_large, cell, thread, dS, eqn)
{
  real source;
  /*tm is referred to the mixture phase*/
  /*ts is is referred to the air-small phase*/
  /*tl is refferd to the air-large phase */
  
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source =  -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP ;
  C_UDMI(cell,tm,0) = source;
  dS[eqn] =  -C_R(cell,tl)/CURRENT_TIMESTEP;
  return source;
}

DEFINE_SOURCE(x_prim_recoil, cell, thread, dS, eqn)
{
  real source;
  /*tm is referred to the mixture phase*/
  /*ts is is referred to the air-small phase*/
  /*tl is refferd to the air-large phase */
  /*tw is refferd to the water phase */
  
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  Thread *tw=THREAD_SUB_THREAD(tm,0);
  source =  (-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP*C_U(cell,tw);
  dS[eqn] =(-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP;
  return source;
  
}

DEFINE_SOURCE(y_prim_recoil, cell, thread, dS, eqn)
{
  real source;
  /*tm is referred to the mixture phase*/
  /*ts is is referred to the air-small phase*/
  /*tl is refferd to the air-large phase */
  /*tw is refferd to the water phase */
  
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *tw=THREAD_SUB_THREAD(tm,0);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source =  (-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP*C_V(cell,tw);
  dS[eqn] =(-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP;
  return source;
  
}

DEFINE_SOURCE(z_prim_recoil, cell, thread, dS, eqn)
{
  real source;
  /*tm is referred to the mixture phase*/
  /*ts is is referred to the air-small phase*/
  /*tl is refferd to the air-large phase */
  /*tw is refferd to the water phase */
  
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *tw=THREAD_SUB_THREAD(tm,0);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source =  (-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP*C_V(cell,tw);
  dS[eqn] =(-C_R(cell,ts)*C_VOF(cell,ts)-C_R(cell,tl)*C_VOF(cell,tl))/CURRENT_TIMESTEP;
  return source;
  
}

DEFINE_SOURCE(x_sec_small_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  source = -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP*C_U(cell,ts);
  dS[eqn] =  -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP;
  return source;
}

DEFINE_SOURCE(y_sec_small_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  source = -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP*C_V(cell,ts);
  dS[eqn] =  -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP;
  return source;
}


DEFINE_SOURCE(z_sec_small_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *ts=THREAD_SUB_THREAD(tm,1);
  source = -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP*C_W(cell,ts);
  dS[eqn] =  -C_R(cell,ts)*C_VOF(cell,ts)/CURRENT_TIMESTEP;
  return source;
}

DEFINE_SOURCE(x_sec_large_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source = -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP*C_U(cell,tl);
  dS[eqn] =  -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP;
  return source;
}

DEFINE_SOURCE(y_sec_large_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source = -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP*C_V(cell,tl);
  dS[eqn] =  -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP;
  return source;
}


DEFINE_SOURCE(z_sec_large_recoil, cell, thread, dS, eqn)
{
  real source;
  Thread *tm = THREAD_SUPER_THREAD(thread);
  Thread *tl=THREAD_SUB_THREAD(tm,2);
  source = -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP*C_W(cell,tl);
  dS[eqn] =  -C_R(cell,tl)*C_VOF(cell,tl)/CURRENT_TIMESTEP;
  return source;
}


