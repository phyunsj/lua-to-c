#include <stdio.h>
#include "cl_calc.h"


cl_return_t cl_calc_freq( int in1, int in2, unsigned int *out ) {
    *out = in1 + in2;
    printf("\n[cl_calc_freq] %d + %d = %d\n", in1, in2, *out);
    return 300;
}

cl_return_t cl_calc_alert( int in1, int in2, unsigned int *inout ) {
    printf("\n[cl_calc_alert] %d + %d + %d (inout) =", in1, in2, *inout);
    *inout = in1 + in2 + *inout;
    printf(" %d\n", *inout);
    return 300;
}

cl_return_t cl_calc_read( cl_int16_t  in1, cl_uint16_t in2, cl_uint32_t *out) {
    *out = in1 + in2;
    printf("\n[cl_calc_read] %d + %d = %d\n", in1, in2, *out);
    return 300;
}

cl_return_t cl_calc_write( cl_msg_t  in, cl_bus_t *out ) {

    out->info   = in.addr;
    out->src    = in.flags & in.addr;
    out->dst    = out->src + in.len;
    out->length = in.len;
    out->stride = in.len + 100;
    out->next   = out->src + 32;

    printf("\n[cl_calc_write] msg addr %d, flags %d, len %d", in.addr, in.flags, in.len );
    printf("\n[cl_calc_write] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out->info, out->src, out->dst, out->length, out->stride, out->next );
    return 300;
}

cl_return_t cl_calc_timer( cl_msg_t *in, cl_bus_t *out ) {

    out->info   = in->addr;
    out->src    = in->flags & in->addr;
    out->dst    = out->src + in->len;
    out->length = in->len;
    out->stride = in->len + 100;
    out->next   = out->src + 32;

    printf("\n[cl_calc_timer] msg addr %d, flags %d, len %d", in->addr, in->flags, in->len );
    printf("\n[cl_calc_timer] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out->info, out->src, out->dst, out->length, out->stride, out->next );
    return 300;
}

int cl_calc_filter( cl_msg_t *in, cl_bus_t *out1, cl_bus_t *out2 ) {
    
    out1->info   = in->addr;
    out1->src    = in->flags & in->addr;
    out1->dst    = out1->src + in->len;
    out1->length = in->len;
    out1->stride = in->len + 100;
    out1->next   = out1->src + 32;

    out2->info   = in->addr + 1;
    out2->src    = in->flags & in->addr + 1;
    out2->dst    = out1->src + in->len + 1;
    out2->length = in->len + 1;
    out2->stride = in->len + 100 + 1;
    out2->next   = out1->src + 32 + 1;

    printf("\n[cl_calc_filter] msg addr %d, flags %d, len %d", in->addr, in->flags, in->len );
    printf("\n[cl_calc_filter:1] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out1->info, out1->src, out1->dst, out1->length, out1->stride, out1->next );
    printf("[cl_calc_filter:2] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out2->info, out2->src, out2->dst, out2->length, out2->stride, out2->next );
    return 300;
}

void cl_calc_serial( cl_msg_t *in1, cl_msg_t *in2, cl_bus_t *out ) {
    
    out->info   = in1->addr;
    out->src    = in1->flags & in1->addr;
    out->dst    = out->src + in1->len;
    out->length = in1->len;
    out->stride = in1->len + 100;
    out->next   = out->src + 32;

    printf("\n[cl_calc_serial:1] msg addr %d, flags %d, len %d", in1->addr, in1->flags, in1->len );
    printf("\n[cl_calc_serial:2] msg addr %d, flags %d, len %d", in2->addr, in2->flags, in2->len );
    
    in2->addr  = in1->addr + 5;
    in2->flags = in1->flags + 10;
    in2->len   = in1->len + 15;

    printf("\n[cl_calc_serial] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out->info, out->src, out->dst, out->length, out->stride, out->next );   
    return ;
}

int cl_calc_servo( cl_msg_t *inout, cl_bus_t *out ) { 
    
    out->info   = inout->addr;
    out->src    = inout->flags & inout->addr;
    out->dst    = out->src + inout->len;
    out->length = inout->len;
    out->stride = inout->len + 100;
    out->next   = out->src + 32;
    printf("\n[cl_calc_servo:before] msg addr %d, flags %d, len %d", inout->addr, inout->flags, inout->len );
    inout->addr  = inout->addr + 5;
    inout->flags = inout->flags + 10;
    inout->len   = inout->len + 15;
    printf("\n[cl_calc_servo:after] msg addr %d, flags %d, len %d", inout->addr, inout->flags, inout->len );
    printf("\n[cl_calc_servo] bus info %d, src %d, dst %d, length %d, stride %d, next %d\n", out->info, out->src, out->dst, out->length, out->stride, out->next );
    return 300;
}

cl_return_t cl_calc_set( cl_int16_t  in1, cl_uint32_t in2, cl_uint16_t *out) {
    *out = in1 + in2;
    printf("\n[cl_calc_set] %d + %d = %d\n", in1, in2, *out);
    return 301; /* always return an error for testing  */
}


