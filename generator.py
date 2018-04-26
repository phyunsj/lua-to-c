#!/usr/bin/python

from __future__ import print_function
from pprint import pprint
from string import Template
import argparse
import sys, os

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

scriptpath = "./codeTemplate.py"
sys.path.append(os.path.abspath(scriptpath))
from codeTemplate import *


class FuncCallVisitor(c_ast.NodeVisitor):
    def __init__(self):
        # [ { name : xxx, return : xxx, params : [ { name : xxx, ref : 0 }, ...] }, ... ]
        self.functions = []
        self.typedefs = []
        self.typedefs_struct = []
        self.primitive_types = ['void', 'short','int','long','unsigned short','unsigned int', 'unsigned long']

    def search_typedef( self, type_name) :       
        for item in self.typedefs :
            #print(item)
            if item['name'] == type_name :
                return item['type_origin']
        return 'unknown'

    def dump(self):
        return { 'func' : self.functions , 'typedef' : self.typedefs, 'typedef-struct' : self.typedefs_struct }

    def visit_FuncDecl (self, node):
        #if isinstance(node, c_ast.FuncDecl):
        #   pass
        func = {}
        params = []
        # parameter
        if isinstance(node.args, c_ast.ParamList):
            unnamed_counter = 10
            for param in node.args.params :
                ptr = 0
                args_list = { 'ptr' : 0 }  
                if isinstance(param, c_ast.Decl): 
                   # named parameter
                   args_list['direction'] = param.name
                else:
                   args_list['direction'] = 'in'+str(unnamed_counter) # c_ast.Typename
                   unnamed_counter =  unnamed_counter + 1

                if isinstance(param.type, c_ast.PtrDecl):
                      args_list['ptr'] = 1
                      args_list['type'] = ' '.join(param.type.type.type.names)
                if isinstance(param.type, c_ast.TypeDecl):
                      args_list['type'] = ' '.join(param.type.type.names)

                params.append(args_list)

        func['params'] = params
        # function name
        if isinstance(node.type, c_ast.TypeDecl):
            #print("TypeDecl:", node.type.declname )
            func['name'] = node.type.declname
            # return type
            if isinstance(node.type.type, c_ast.IdentifierType):
                #print("IdentifierType:", node.type.type.names[0] )
                func['return'] = ' '.join(node.type.type.names)
        self.functions.append(func)

    def visit_TypeDecl (self, node):
        typedef = {}
        params = []
        if isinstance(node.type, c_ast.IdentifierType):
            typedef['name'] = node.declname
            typedef['type'] = ' '.join(node.type.names)
            if typedef['type'] in self.primitive_types :
               typedef['type_origin'] = typedef['type']
            else:
               # find from self.typedefs
               typedef['type_origin'] = self.search_typedef( typedef['type'] )
            self.typedefs.append(typedef)
        elif isinstance(node.type, c_ast.Struct):
            typedef['name'] = node.type.name
            for param in node.type.decls :
                params.append( { 'name' : param.type.declname ,'type' : ' '.join(param.type.type.names) })
            typedef['type'] = params
            self.typedefs_struct.append(typedef)
            typedef['type_origin'] = 'struct'
            self.typedefs.append(typedef)
        else:
            pass     



class CodeGenerator ( codeTemplate ):
    def __init__ (self, symtab) :
        self.product = 'CL'
        self.product_lib_name = 'cl_calc'
        self.symtab  = symtab
        self.primitive_types = ['void', 'short','int','long','unsigned short','unsigned int', 'unsigned long']

    def search_type(self, searchType) :
        for typedef in  self.symtab['typedef'] :
            if typedef['name'] == searchType : 
                if typedef['type_origin'] != 'struct' :
                    return typedef['type_origin']
                else:
                    return typedef['name']+'_s'
        # primitive type already. just return it
        return searchType 
    
    def find_type(self, searchType) :
        if searchType in self.primitive_types :
           return 1
        for typedef in  self.symtab['typedef'] :
            if typedef['name'] == searchType : 
                if typedef['type_origin'] in self.primitive_types :
                    return 1
                else:
                    return 0
        return 0

    def print_pointer(self, ptr) :
        if ptr == 1 :
           return '*'
        else:
           return ''

    def print_void(self, ptr) :
        if ptr == 'void' :
           return ' 300; '
        else:
           return ''
    
    def print_ref(self, ptr) :
        if ptr == 1 :
           return ''
        else:
           return '&'

    def print_r_ref(self, ptr) :
        if ptr == 1 :
           return '&'
        else:
           return ''

    def print_comma(self, idx) :
        if idx == 0 :
           return ''
        else:
           return ','

    def print_ret(sefl, type) :
        if type == 'void' :
           return '300; (void)'
        else:
           return ''

    def print_getfield_stmt(self, param_name, field_name, field_type, stack_index) :
        # More can be done for field_type
        stmt = '\n\t\tlua_getfield(L, '+str(stack_index)+', "'+field_name +'");'
        stmt = stmt + '\n\t\tSTACK_DUMP(L);'
        stmt = stmt + '\n\t\tif( lua_type(L, -1) == LUA_TNIL ) { '+self.print_err_stmt (301) +'}'
        stmt = stmt + '\n\t\t'+param_name+'.'+field_name+' = lua_tonumber(L, -1); lua_pop(L, 1);' 
        stmt = stmt + '\n\t\tSTACK_DUMP(L);'
        return stmt

    def print_setfield_stmt(self, param_name, field_name, field_type) :
        stmt = '\n\tlua_pushstring(L, "'+field_name +'");  /* push key */'
        stmt = stmt + '\n\tSTACK_DUMP(L);'
        stmt = stmt + '\n\tlua_pushnumber(L, '+param_name+'.'+field_name+');  /* push value */'
        stmt = stmt + '\n\tSTACK_DUMP(L);'
        stmt = stmt + '\n\tlua_settable(L, -3);'
        stmt = stmt + '\n\tSTACK_DUMP(L);'
        return stmt
        

    def print_err_stmt(sefl, errcode) :
        stmt = '\n\t\t\terrcode = 301; /* not supported types */'
        stmt = stmt +'\n\t\t\tlua_pushnumber( L, errcode );'
        stmt = stmt +'\n\t\t\tSTACK_DUMP(L);'
        stmt = stmt +'\n\t\t\treturn 1;'
        return stmt 

    def gen_func_register(self):
        self.lib_main  = open('./'+self.product.upper()+'_LUA.c', 'w')  
        self.lib_wrapper = open('./'+self.product.upper()+'_LUA.include', 'w')

        func_list = ''
        # func
        for idx, func in  enumerate(self.symtab['func']) :
            num_result = 1 # at least 1 result
            arg_list = ''
            param_list = ''
            fetch_stmt = ''
            push_stmt = ''
            func_list = func_list + '\n\t\t{"'+func['name']+'" , l_'+func['name']+'},'
            req_counter = 1
            for idx2, param in enumerate(func['params']):

                
                if param['direction'].startswith('in') and not param['direction'].startswith('inout'):
                    if self.find_type(param['type']) :
                        arg_list = arg_list +  self.print_comma(idx2) +  param['direction']
                        param_list =  param_list + '\n\t' +param['type']+' '+param['direction']+';'
                        fetch_stmt = fetch_stmt +'\n\t'+param['direction']+' =  luaL_checknumber ( L, '+str(req_counter)+' );'
                    else:
                        arg_list = arg_list +  self.print_comma(idx2) + self.print_r_ref(param['ptr']) + param['direction']
                        param_list =  param_list + '\n\t' +param['type']+' '+param['direction']+';'
                        fetch_stmt = fetch_stmt + '\n\tif (lua_type( L, '+str(req_counter)+' ) == LUA_TTABLE ) {'
                        for udata_type in self.symtab['typedef-struct'] :
                            if param['type'] == udata_type['name'] :
                                for udata_member in udata_type['type'] :
                                    fetch_stmt = fetch_stmt + self.print_getfield_stmt( param['direction'], udata_member['name'], udata_member['type'], req_counter)
                        fetch_stmt = fetch_stmt + '\n\t} else {'+self.print_err_stmt(301)+'\n\t}'
                    req_counter = req_counter + 1

                if param['direction'].startswith('inout'):
                    if self.find_type(param['type']) :
                        arg_list = arg_list +  self.print_comma(idx2) + self.print_r_ref(param['ptr']) + param['direction']
                        param_list =  param_list + '\n\t' +param['type']+' '+param['direction']+';'
                        fetch_stmt = fetch_stmt +'\n\t'+param['direction']+' =  luaL_checknumber ( L, '+str(req_counter)+' );'
                        push_stmt = push_stmt + '\n\tlua_pushnumber( L, '+param['direction']+' );'
                    else:
                        arg_list = arg_list +  self.print_comma(idx2) +  self.print_r_ref(param['ptr']) + param['direction']
                        param_list =  param_list + '\n\t' +param['type']+' '+param['direction']+';'
                        
                        fetch_stmt = fetch_stmt + '\n\tif (lua_type( L, '+str(num_result)+' ) == LUA_TTABLE ) {'
                        for udata_type in self.symtab['typedef-struct'] :
                            if param['type'] == udata_type['name'] :
                                for udata_member in udata_type['type'] :
                                    fetch_stmt = fetch_stmt + self.print_getfield_stmt( param['direction'], udata_member['name'], udata_member['type'],  req_counter )
                        fetch_stmt = fetch_stmt + '\n\t} else {'+self.print_err_stmt(301)+'\n\t}'

                        push_stmt = push_stmt + '\n\tlua_newtable (L); /* create new table */'
                        for udata_type in self.symtab['typedef-struct'] :
                            if param['type'] == udata_type['name'] :
                                for udata_member in udata_type['type'] :
                                    push_stmt = push_stmt + self.print_setfield_stmt( param['direction'], udata_member['name'], udata_member['type'])

                    req_counter = req_counter + 1
                    num_result = num_result + 1

                if  param['direction'].startswith('out'):
                    
                    if self.find_type(param['type']) :
                        arg_list = arg_list +  self.print_comma(idx2) +  self.print_r_ref(param['ptr']) +param['direction']
                        param_list =  param_list + '\n\t' +param['type']+' '+ param['direction']+';'
                        push_stmt = push_stmt + '\n\tlua_pushnumber( L, '+param['direction']+' );'
                    else:
                        arg_list = arg_list +  self.print_comma(idx2) +   self.print_r_ref(param['ptr']) + param['direction']
                        param_list = param_list + '\n\t'+param['type']+' '+param['direction'] +';'
                        
                        push_stmt = push_stmt + '\n\tlua_newtable (L);/* create new table */'
                        for udata_type in self.symtab['typedef-struct'] :
                            if param['type'] == udata_type['name'] :
                                for udata_member in udata_type['type'] :
                                    push_stmt = push_stmt + self.print_setfield_stmt( param['direction'], udata_member['name'], udata_member['type'])
                    num_result = num_result + 1
            

            stmt = Template(self.lua_wrapper_routine).safe_substitute( dict( \
                        func_name=func['name'], \
                        num_result=num_result, \
                        arg_list=arg_list, \
                        param_list=param_list, \
                        fetch_stmt=fetch_stmt, \
                        push_stmt=push_stmt, \
                        return_stmt=self.print_ret(func['return']) \
                         ))
            self.lib_wrapper.write(stmt)

        stmt = Template(self.lua_c_library).safe_substitute( dict( \
                        LIB_NAME=self.product.upper(), \
                        lib_name=self.product_lib_name, \
                        func_list=func_list \
                         ))
        self.lib_main.write( stmt ) 
        self.lib_main.close()

        self.lib_wrapper.close()

    def gen(self):
        self.gen_func_register()



if __name__ == "__main__":
    argparser = argparse.ArgumentParser('Scan AST & Create Symbol Table')
    argparser.add_argument('filename', help='name of file to parse')
    args = argparser.parse_args()

    ast = parse_file(args.filename, use_cpp=False)
    #ast.show()
    #for (child_name, child) in ast.children():
    #        child.show( sys.stdout ,
    #           offset= 2,
    #            attrnames=True,
    #            nodenames=True,
    #            showcoord=True,
    #            _my_node_name=child_name)

    v = FuncCallVisitor()
    v.visit(ast)
    #pprint(v.dump())

    lua = CodeGenerator( v.dump() )
    lua.gen()

    

