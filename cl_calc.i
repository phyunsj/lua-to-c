# 1 "cl_calc.h"
# 1 "<built-in>"
# 1 "<command-line>"
# 1 "cl_calc.h"
# 20 "cl_calc.h"
typedef short cl_int16_t;
typedef int cl_int32_t;
typedef long cl_int64_t;
typedef unsigned short cl_uint16_t;
typedef unsigned int cl_uint32_t;
typedef unsigned long cl_uint64_t;





typedef cl_int32_t cl_return_t;





typedef struct cl_msg_t {
   cl_int16_t addr;
   cl_int16_t flags;
   cl_int32_t len;
} cl_msg_t;





typedef struct cl_bus_t {
   cl_int32_t info;
   cl_int32_t src;
   cl_int32_t dst;
   cl_int32_t length;
   cl_int32_t stride;
   cl_int32_t next;

} cl_bus_t;
# 65 "cl_calc.h"
cl_return_t cl_calc_freq( int , int in, unsigned int *out );
# 74 "cl_calc.h"
cl_return_t cl_calc_alert( int , int in, unsigned int *inout );
# 83 "cl_calc.h"
cl_return_t cl_calc_read( cl_int16_t , cl_uint16_t in, cl_uint32_t *out);







cl_return_t cl_calc_write( cl_msg_t in, cl_bus_t *out );







cl_return_t cl_calc_timer( cl_msg_t *in, cl_bus_t *out );
# 108 "cl_calc.h"
int cl_calc_filter( cl_msg_t *in, cl_bus_t *out1 , cl_bus_t *out2);
# 117 "cl_calc.h"
void cl_calc_serial( cl_msg_t *in1, cl_msg_t *in2, cl_bus_t *out );







int cl_calc_servo( cl_msg_t *inout, cl_bus_t *out );
