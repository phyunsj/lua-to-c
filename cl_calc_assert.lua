cl_lib = require 'cl_calc'
print("--- 1.")
errcode , out  = cl_lib.cl_calc_freq(4,5)
assert( errcode  == 300, "cl_calc_freq() errcode != 300" )
assert( out == 9 , "cl_calc_freq() out != 9" )
print("--- 2.")
errcode, out  = cl_lib.cl_calc_alert(4, 5, 10)
assert( errcode  == 300, "cl_calc_alert() errcode != 300" )
assert( out == 19 , "cl_calc_alert() out != 19" )
print("--- 3.")
errcode, out  = cl_lib.cl_calc_read(5, 9)
assert( errcode  == 300, "cl_calc_read() errcode != 300" )
assert( out == 14 , "cl_calc_read() out != 14" )
print("--- 4. errcode == 301. invalid field name.")
-- Invalid field "flag" -> "flags". Expect an error
msg = {}
msg["addr"] = 0x1234
msg["flag"] = 0x0001
msg["len"] = 32
for key,value in pairs(msg) do print(key,value) end
errcode = cl_lib.cl_calc_timer( msg )
assert( errcode == 301, "cl_calc_timer() errcode != 300" )
print("--- 5. in + out")
msg = {}
msg["addr"] = 0x1234
msg["flags"] = 0x0001
msg["len"] = 32
for key,value in pairs(msg) do print("msg:",key,value) end
errcode , bus = cl_lib.cl_calc_timer( msg )
assert( errcode  == 300, "cl_calc_timer() errcode != 300" )
for key,value in pairs(bus) do print("bus:", key,value) end
print("--- 6. in (call-by-value) + out")
msg = {}
msg["addr"] = 0x1234
msg["flags"] = 0x0001
msg["len"] = 32
for key,value in pairs(msg) do print("msg:",key,value) end
errcode , bus = cl_lib.cl_calc_write( msg )
assert( errcode  == 300, "cl_calc_write() errcode != 300" )
for key,value in pairs(bus) do print("bus:",key,value) end
print("--- 7. inout +  out ")
msg = {}
msg["addr"] = 0x1234
msg["flags"] = 0x0001
msg["len"] = 32
for key,value in pairs(msg) do print(key,value) end
errcode , msg1, bus2 = cl_lib.cl_calc_servo( msg )
assert( errcode  == 300, "cl_calc_servo() errcode != 300" )
for key,value in pairs(msg1) do print("msg:",key,value) end
for key,value in pairs(bus2) do print("bus:",key,value) end
print("--- 8. in + out x 2 ")
msg = {}
msg["addr"] = 0x1234
msg["flags"] = 0x0001
msg["len"] = 32
for key,value in pairs(msg) do print( "msg:", key,value) end
errcode , bus1, bus2 = cl_lib.cl_calc_filter( msg )
assert( errcode  == 300, "cl_calc_filter() errcode != 300" )
for key,value in pairs(bus1) do print( "bus1:", key,value) end
for key,value in pairs(bus2) do print( "bus2:", key,value) end
print("--- 9. in x 2 + out ")
msg1 = {}
msg1["addr"] = 0x1234
msg1["flags"] = 0x0001
msg1["len"] = 32
msg2 = {}
msg2["addr"] = 0x1235
msg2["flags"] = 0x0002
msg2["len"] = 33
for key,value in pairs(msg1) do print("msg1:", key,value) end
for key,value in pairs(msg2) do print("msg2:",key,value) end
errcode , bus  = cl_lib.cl_calc_serial( msg1, msg2 )
assert( errcode  == 300, "cl_calc_serial() errcode != 300" )
for key,value in pairs(bus) do print( "bus:", key,value) end
assert( bus["length"]  == 32, "cl_calc_serial() bus[length] != 32" )
print("--- done")




