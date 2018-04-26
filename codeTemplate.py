#!/usr/bin/env python

class codeTemplate(object):

    def __init__ (self):
        pass
    
    lua_wrapper_routine = '''

static int l_${func_name} (lua_State *L) {
    
    //check and fetch the arguments
    int errcode = 0;
    ${param_list}

    STACK_DUMP(L);
    ${fetch_stmt}

    errcode = ${return_stmt} ${func_name}(${arg_list});
    
    //push the results
    lua_pushnumber( L, errcode ); // errcode first
    STACK_DUMP(L);

    ${push_stmt}
  
    //return number of results
    STACK_DUMP(L);
    return ${num_result};
}
'''

    lua_c_library = '''

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

#include "${lib_name}.h"

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
          printf("\\"%s\\"", lua_tostring(L, i));
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
  printf("]\\n");
}


#include "${LIB_NAME}_LUA.include"

static const struct luaL_Reg ${LIB_NAME}_REGISTER [] = {
      ${func_list}
      {NULL, NULL}  
    };

int luaopen_${lib_name} (lua_State *L){
    luaL_newlib(L, ${LIB_NAME}_REGISTER);
    return 1;
}

#ifdef __cplusplus
}
#endif

'''

