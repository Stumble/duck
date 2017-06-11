import clang.cindex
from clang.cindex import CursorKind
import sys
import json

# helper functions
is_from_main_file = clang.cindex.conf.lib.clang_Location_isFromMainFile
is_in_system_header = clang.cindex.conf.lib.clang_Location_isInSystemHeader

# a dict from className to classInformation
g_classes = {}
g_final_result = {}

class cxxClass:
    def __init__(self, name, base_list):
        """
        global name of the class
        its parents [] of global name
        """
        self.name = name
        self.base_list = base_list
        self.functions = {}
        self.fields = {}
        self.implemented = False

    def convert_to_json_dict(self):
        rtn = {}
        rtn['base_list'] = self.base_list
        rtn['fields'] = self.fields
        methods = {}
        for (k, v) in self.functions.iteritems():
            methods[k] = v.convert_to_json_dict()
        rtn['methods'] = methods
        return rtn

    def setImplementedFunction(self, f):
        # Todo: check if it's already there
        self.implemented = True
        self.functions[f.name] = f

    def setFunction(self, f):
        # Todo: check if it's already there
        self.functions[f.name] = f

    def addField(self, name, type_name):
        # TODO
        # if it's not a record, don't add class prefix
        self.fields[name] = type_name

    def __repr__(self):
        return self.name + " : " + str(self.base_list) + "\n" + str(self.functions)


class cxxFunction:
    def __init__(self, name, parameters, rtn_type):
        """
        (str) function name
        (list) its parameter list
        """
        self.name = name
        self.parameters = parameters
        self.call_list = []
        self.n_lines_of_code = 0
        self.return_type = rtn_type

    def convert_to_json_dict(self):
        rtn = {}
        # TODO
        # implement following functions
        rtn['run-time-invokes'] = 0
        rtn['linesOfCode'] = self.n_lines_of_code
        rtn['calling-function'] = self.call_list
        rtn['parameter'] = self.parameters
        rtn['return_type'] = self.return_type
        return rtn

    def addCall(self, calledFunction):
        # calledFunction: str
        call_list += calledFunction

    def __repr__(self):
        return self.name + " " + str(self.parameters) + " " + str(self.n_lines_of_code)


def getFullClassName(cc):
    cls_name = cc.displayname
    cc_iter = cc
    parents = [cls_name]
    while True:
        try:
            parent_cc = cc_iter.semantic_parent
            parents.append(parent_cc.displayname)
            cc_iter = parent_cc
        except Exception:
            break
    parents = parents[:-1]
    parents.reverse()
    return "class " + "::".join(parents)

def extract_function_return_type(cursor):
    return "class " + drop_qualifier_and_pointer(cursor.result_type.spelling)

def processInClassFuncDecl(cursor):
    parameter_list = {}
    anonymous_parameter_cnt = 0
    for cc in cursor.get_children():
        if cc.kind == CursorKind.PARM_DECL:
            pure_type_name = drop_qualifier_and_pointer(cc.type.spelling)
            if cc.displayname:
                parameter_list[cc.displayname] = "class " + pure_type_name
            else:
                parameter_list[str(anonymous_parameter_cnt)] = "class " + pure_type_name
                anonymous_parameter_cnt += 1
        else:
            # TODO
            # process if they prefer to
            # declare function in header file
            pass
    return parameter_list

def remove_keyword_in_string(target, keyword):
    # TODO
    # this will remove keyword in **keyword**
    # should check whether before end with space
    # or after start with space
    rtn = ""
    while True:
        (before, cls, after) = target.partition(keyword)
        rtn += before
        if after:
            target = after
        else:
            break
    return rtn

def drop_qualifier_and_pointer(full_type_name):
    id_list = ['const', 'volatile', 'mutable', '*', '&']
    for kw in id_list:
        full_type_name = remove_keyword_in_string(full_type_name, kw)
    return full_type_name.strip()

# this function will remove all "class " in the string
# input: str
# rtn  : str
def remove_class_prefix(full_name):
    rtn = ""
    while True:
        (before, cls, after) = full_name.partition('class ')
        rtn += before
        if after:
            full_name = after
        else:
            break
    return rtn

def processClassDecl(cursor):
    class_name = getFullClassName(cursor)
    class_base_list = []
    for cc in cursor.get_children():
        if cc.kind != CursorKind.CXX_BASE_SPECIFIER:
            continue
        class_base_list.append(cc.displayname)

    cls = cxxClass(class_name, class_base_list)

    # add class to global dict
    g_classes[class_name] = cls

    # process each function
    for cc in cursor.get_children():
        if cc.kind == CursorKind.CXX_METHOD:
            rtn_type = extract_function_return_type(cc)
            para_list = processInClassFuncDecl(cc);
            funcName = cc.displayname
            cls.setFunction(cxxFunction(funcName, para_list, rtn_type))
        elif cc.kind == CursorKind.FIELD_DECL:
            # print "playing with:" + str(cc.displayname)
            pure_type_name = drop_qualifier_and_pointer(cc.type.spelling)
            cls.addField(cc.displayname, "class " + pure_type_name)
            # print cc.get_definition()
            # print cc.get_usr()
            # for hint in cc.walk_preorder():
            #     print cc.displayname + " : " + str(cc.kind)
        else:
            pass

def processStandaloneFuncDecl(cursor):
# function_name =     #
    function_name = cursor.displayname
    n_lines_of_code = cursor.extent.end.line - cursor.extent.start.line + 1
    belonged_class_name = ""
    parameter_list = {}
    rtn_type = extract_function_return_type(cursor)

    for cc in cursor.get_children():
        if cc.kind == CursorKind.TYPE_REF:
            belonged_class_name = cc.displayname
        elif cc.kind == CursorKind.PARM_DECL:
            pure_type_name = drop_qualifier_and_pointer(cc.type.spelling)
            parameter_list[cc.displayname] = "class " + pure_type_name
        elif cc.kind == CursorKind.COMPOUND_STMT:
            # due to cpp's complicated func call
            # smart pointer, dynamic dispatch
            # we skipped this function now
            pass
            # print "----------- using "
            # print function_name
            # for stmt in cc.get_children():
            #     if stmt.kind == CursorKind.CALL_EXPR:
            #         print str(stmt.kind) + " : " + str(stmt.displayname)
            #         print "hints: "
            #         for hint in stmt.walk_preorder():
            #             print str(hint.kind) + " : " + hint.displayname
            #     # elif stmt.kind == CursorKind.
            # print "-----------"
        else:
            pass

    updated_func = cxxFunction(function_name, parameter_list, rtn_type)
    updated_func.n_lines_of_code = n_lines_of_code

    if belonged_class_name in g_classes:
        cls = g_classes[belonged_class_name]
        if not (function_name in cls.functions):
            pass
            # raise Exception("function not found: " + function_name)
        cls.setImplementedFunction(updated_func)
        # cls.functions[function_name] =
    else:
        sys.stderr.write("[class not exist]: function:" + function_name + " class:" + belonged_class_name + "\n")
        # raise Exception("[class not exist]: function:" + function_name + " class:" + belonged_class_name)

# ==============================================================================
# execution begin here

def work(cursor):
   for cc in cursor.walk_preorder():
       if not is_in_system_header(cc.location) and cc.is_definition():
           if cc.kind == CursorKind.CLASS_DECL:
               processClassDecl(cc)
           elif cc.kind == CursorKind.FUNCTION_DECL:
               sys.stderr.write("ignored non-class_member function : " + cc.displayname + "\n")
           elif cc.kind == CursorKind.CXX_METHOD:
                    # usually, it should be the class method definition
                    # in the .cpp file
               processStandaloneFuncDecl(cc)



# initialization of reading
if len(sys.argv) > 1:
    for inputAst in sys.argv[1:]:
        idx = clang.cindex.Index.create()
        tu = idx.read(inputAst)
        cursor = tu.cursor
        work(cursor)
        for (k, v) in g_classes.iteritems():
            if v.implemented:
                g_final_result[k] = v
        # clean global variable
        g_classes = {}
else:
    raise Exception("no input files")

def final_dump():
    rtn = {}
    class_all = {}
    for (k, v) in g_final_result.iteritems():
        class_all[k] = v.convert_to_json_dict();
    rtn['classes'] = class_all
    # print json.dumps(rtn)
    print json.dumps(rtn, indent=2)

final_dump()

# init global variable
# tu = idx.parse('sample.cpp', args=['-std=c++11'],
#                 unsaved_files=[('tmp.cpp', s)],  options=0)


# for (k, v) in g_classes.iteritems():
#     print v
#     print ""

# json.dumps(myobject.__dict__)


# for t in tu.get_tokens(extent=tu.cursor.extent):
#     print (t.kind)


# An expression that calls a function.
# CursorKind.CALL_EXPR = CursorKind(103)

# A C++ class method.
# CursorKind.CXX_METHOD = CursorKind(21)

# A C++ namespace.
# CursorKind.NAMESPACE = CursorKind(22)

# A C++ constructor.
# CursorKind.CONSTRUCTOR = CursorKind(24)

# A C++ destructor.
# CursorKind.DESTRUCTOR = CursorKind(25)

# A function or method parameter.
# CursorKind.PARM_DECL = CursorKind(10)
