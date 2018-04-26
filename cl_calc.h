/**
 * @file cl_calc.h
 * @author phyunsj@yahoo.com
 * @date April 2018
 * @brief File containing example of calc functions with vairous input/output types.
 * \n\n ONC RPC restricted us to use remote procedures that accept a single parameter and 
 * return a single parameter. Later versions might support multiple parameters.
 * \n\n The name of parameter informs where it belongs to : request or response.
 * \n 1. IDL should define a RPC request with [in] and [inout]
 * \n 2. IDL should define a RPC response with [inout] and [out]  
 *
**/
#ifndef _CL_CALC_
#define _CL_CALC_
/**
 * @brief platform-specific data types.
 *
 */

typedef short cl_int16_t; 
typedef int   cl_int32_t;
typedef long  cl_int64_t; 
typedef unsigned short cl_uint16_t; 
typedef unsigned int   cl_uint32_t;
typedef unsigned long  cl_uint64_t; 

/**
 * @brief return types.
 *
 */
typedef cl_int32_t cl_return_t;

/**
 * @brief user-defined request struct type.
 *
 */
typedef struct cl_msg_t {
   cl_int16_t addr;  
   cl_int16_t flags;
   cl_int32_t len;   
} cl_msg_t;

/**
 * @brief user-defined response struct type.
 *
 */
typedef struct cl_bus_t {
   cl_int32_t info;
   cl_int32_t src;
   cl_int32_t dst;
   cl_int32_t length;
   cl_int32_t stride;
   cl_int32_t next;
   //cl_int32_t pad[2];
} cl_bus_t;

/**
* @brief calculation 1. 2 inputs X 1 output.
*
* @param [in]  None - the first input parameter.
* @param [in]  in - the second input parameter.
* @param [out] out - the output parameter after calculation. 
* @return cl_return_t SUCCESS or error code.
*/
cl_return_t cl_calc_freq( int , int in, unsigned int *out );
/**
* @brief calculation 2. 2 inputs X 1 output. Unnamed parameter becomes [in]
*
* @param [in]  None - the first input parameter.
* @param [in]  in - the second input parameter.
* @param [in]  [out] inout - the third input parameter & the output parameter after calculation. 
* @return cl_return_t SUCCESS or error code.
*/
cl_return_t cl_calc_alert( int , int in, unsigned int *inout );
/**
* @brief calculation 3. 2 inputs X 1 output.
*
* @param [in]  None - the first input parameter.
* @param [in]  in - the second input parameter.
* @param [out] out - the output parameter after calculation. 
* @return cl_return_t SUCCESS or error code.
*/
cl_return_t cl_calc_read( cl_int16_t , cl_uint16_t in, cl_uint32_t *out);
/**
* @brief calculation 4. 1 inputs X 1 output
*
* @param [in]  in - the input parameter.
* @param [out] out - the output parameter after calculation. 
* @return cl_return_t SUCCESS or error code.
*/
cl_return_t cl_calc_write( cl_msg_t  in, cl_bus_t *out );
/**
* @brief calculation 5. 1 inputs X 1 output
*
* @param [in]  in - the input parameter.
* @param [out] out - the output parameter after calculation. 
* @return cl_return_t SUCCESS or error code.
*/
cl_return_t cl_calc_timer( cl_msg_t *in, cl_bus_t *out );
/**
* @brief calculation 6. 1 inputs X 1 output
*
* @param [in]  in - the input parameter.
* @param [out] out1 - the output parameter after calculation. 
* @param [out] out2 - the output parameter after calculation. 
* @return int SUCCESS or error code.
*/
int  cl_calc_filter( cl_msg_t *in, cl_bus_t *out1 , cl_bus_t *out2);
/**
* @brief calculation 7. 1 inputs X 1 output
*
* @param [in]  in1 - the input parameter.
* @param [in]  in2 - the input parameter.
* @param [out] out - the output parameter after calculation. 
* @return void.
*/
void cl_calc_serial( cl_msg_t *in1, cl_msg_t *in2, cl_bus_t *out );
/**
* @brief calculation 8. 1 inputs X 2 output
*
* @param [in] [out] inout - the input parameter & output parameter.
* @param [out]   out   - the output parameter after calculation. 
* @return int SUCCESS or error code.
*/
int  cl_calc_servo( cl_msg_t *inout, cl_bus_t *out );


#endif /* _CL_CALC_ */