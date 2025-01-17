/* This file generated automatically. */
/*          Do not modify.            */
#include "udf.h"
#include "prop.h"
#include "dpm.h"
extern DEFINE_SOURCE(degassing_source_small, cell, thread, dS, eqn);
extern DEFINE_SOURCE(degassing_source_large, cell, thread, dS, eqn);
extern DEFINE_SOURCE(x_prim_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(y_prim_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(z_prim_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(x_sec_small_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(y_sec_small_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(z_sec_small_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(x_sec_large_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(y_sec_large_recoil, cell, thread, dS, eqn);
extern DEFINE_SOURCE(z_sec_large_recoil, cell, thread, dS, eqn);
__declspec(dllexport) UDF_Data udf_data[] = {
{"degassing_source_small", (void(*)())degassing_source_small, UDF_TYPE_SOURCE},
{"degassing_source_large", (void(*)())degassing_source_large, UDF_TYPE_SOURCE},
{"x_prim_recoil", (void(*)())x_prim_recoil, UDF_TYPE_SOURCE},
{"y_prim_recoil", (void(*)())y_prim_recoil, UDF_TYPE_SOURCE},
{"z_prim_recoil", (void(*)())z_prim_recoil, UDF_TYPE_SOURCE},
{"x_sec_small_recoil", (void(*)())x_sec_small_recoil, UDF_TYPE_SOURCE},
{"y_sec_small_recoil", (void(*)())y_sec_small_recoil, UDF_TYPE_SOURCE},
{"z_sec_small_recoil", (void(*)())z_sec_small_recoil, UDF_TYPE_SOURCE},
{"x_sec_large_recoil", (void(*)())x_sec_large_recoil, UDF_TYPE_SOURCE},
{"y_sec_large_recoil", (void(*)())y_sec_large_recoil, UDF_TYPE_SOURCE},
{"z_sec_large_recoil", (void(*)())z_sec_large_recoil, UDF_TYPE_SOURCE},
};
__declspec(dllexport) int n_udf_data = sizeof(udf_data)/sizeof(UDF_Data);
#include "version.h"
__declspec(dllexport) void UDF_Inquire_Release(int *major, int *minor, int *revision)
{
  *major = RampantReleaseMajor;
  *minor = RampantReleaseMinor;
  *revision = RampantReleaseRevision;
}
