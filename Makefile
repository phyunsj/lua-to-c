CROSS_COMPILE=
CC=$(CROSS_COMPILE)gcc

all:  clean cpp  codegen calc 

debug:  clean cpp  codegen calc_debug 

cpp:
	cpp cl_calc.h -o cl_calc.i

codegen:
	python generator.py  cl_calc.i

calc: 
	$(CC) --version
	$(CC) cl_calc.c CL_LUA.c -shared -o cl_calc.so -fPIC -llua5.2 -I. -I/usr/include/lua5.2

calc_debug: 
	$(CC) --version
	$(CC) cl_calc.c CL_LUA.c -DDEBUG -shared -o cl_calc.so  -fPIC -llua5.2 -I. -I/usr/include/lua5.2

clean:
	rm -f *.o *.so *.pyc
