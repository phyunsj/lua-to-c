

#ifdef __cplusplus
  #include "lua.hpp"
#else
  #include "lua.h"
  #include "lualib.h"
  #include "lauxlib.h"
#endif

#ifdef DEBUG
#define STACK_DUMP(a) stackDump(a)
#else
#define STACK_DUMP(a) 
#endif

#ifdef __cplusplus
extern "C"{
#endif

#include "cl_calc.h"

static void stackDump ( lua_State *L ) {
  int i;
  int top = lua_gettop(L);
  printf("S[ ");
  for(i=1; i<=top; i++) {
    int t = lua_type(L, i);
    switch(t) {
      case LUA_TNUMBER: {
          printf("%g", lua_tonumber(L, i));
          break;
      }
      case LUA_TSTRING: {
          printf("\"%s\"", lua_tostring(L, i));
          break;
      }
      case LUA_TTABLE: {
          printf("%s", lua_typename(L, t));
          break;
      }
      default : {
          printf("%s", lua_typename(L, t));
      }
    }
    printf(" ");
  }  
  printf("]\n");
}


#include "CL_LUA.include"

static const struct luaL_Reg CL_REGISTER [] = {
      
		{"cl_calc_freq" , l_cl_calc_freq},
		{"cl_calc_alert" , l_cl_calc_alert},
		{"cl_calc_read" , l_cl_calc_read},
		{"cl_calc_write" , l_cl_calc_write},
		{"cl_calc_timer" , l_cl_calc_timer},
		{"cl_calc_filter" , l_cl_calc_filter},
		{"cl_calc_serial" , l_cl_calc_serial},
		{"cl_calc_servo" , l_cl_calc_servo},
      {NULL, NULL}  
    };

int luaopen_cl_calc (lua_State *L){
    luaL_newlib(L, CL_REGISTER);
    return 1;
}

#ifdef __cplusplus
}
#endif

