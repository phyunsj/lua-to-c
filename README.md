# Lua-to-C 

#### Generate Lua-to-C wrapper out of `*.h` directly.

Suggested readings for "calling C functions from Lua":
- https://chsasank.github.io/lua-c-wrapping.html
- http://lua-users.org/wiki/BindingCodeToLua
- http://acamara.es/blog/2012/08/calling-c-functions-from-lua-5-2/
- https://www.cs.usfca.edu/~galles/cs420/lecture/LuaLectures/LuaAndC.html

## cl_calc_xxxx ( ... )

`cl_calc.c` Just random funtions for the test. `C struct` is mapped to `lua table` and vice versa.

## Code Generation

Start with extracting `FuncDecl` by visiting AST (created by **pycparser**). 

The following files are generated :

- `CL_LUA.c`
- `CL_LUA.include`

## Build & Run

```
$ make 
$ lua -i -e "_PROMPT='lua$ '"
Lua 5.2.0  Copyright (C) 1994-2011 Lua.org, PUC-Rio
lua$
lua$ dofile("cl_calc_test.lua")
...
lua$
```

if you wish to display the virtual stack, type **make debug** instead

## Closing Remarks

This is a proof of concept to demonstrate testing C fuctions with help of **lua** (stand-alone ) interpreter (+ **pycparser** + code generator).

