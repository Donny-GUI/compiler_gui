import sys
import os
import ast
import dis


from opcode import *
from opcode import __all__ as _opcodes_all

from importlib.util import (
    cache_from_source, 
    source_hash, 
    source_from_cache
)
from dis import Bytecode
from py_compile import (
    _get_default_invalidation_mode, 
    PyCompileError, 
    PycInvalidationMode
)
from importlib.machinery import SourceFileLoader
from typing import Any

from importlib._bootstrap_external import (
    _calc_mode, 
    _write_atomic, 
    _code_to_timestamp_pyc, 
    _code_to_hash_pyc
)



class VerbosityLevel(int):
    def __init__(self, value: int) -> None:
        self.value = value
        super().__init__()

class OptimizationLevel(int):
    def __init__(self, value) -> None:
        self.value = value
        super().__init__()
        
class Optimization:
    levels = [-2, -1, 0, 1 , 2]
    current_interpreter = OptimizationLevel(levels[1])
    
    
class Verbosity:
    levels = [0, 1, 2]
    full   = VerbosityLevel(levels[0])
    errors = VerbosityLevel(levels[1])
    none   = VerbosityLevel(levels[2])


class PythonBytecode(Bytecode):
    def __init__(self, file: str, 
                 cfile: str=None, 
                 dfile: str=None, 
                 doraise: bool=False, 
                 optimize: OptimizationLevel = Optimization.current_interpreter, 
                 invalidation_mode=None, 
                 quiet: VerbosityLevel = Verbosity.full) -> None:
        """ Takes a filepath and creates and saves the bytecode

        Args:
            file (str): filepath to the file
            
            cfile (str, optional): 
                                The target byte compiled file name.  When not given, this
                                defaults to the PEP 3147/PEP 488 location.
                                Defaults to None.
                                
            dfile (str, optional): 
                                Purported file name, i.e. the file name that shows up in
                                error messages.  Defaults to the source file name.
                                Defaults to None.
                                
            doraise (bool, optional): 
                                Flag indicating whether or not an exception should be
                                raised when a compile error is found.  If an exception occurs and this
                                flag is set to False, a string indicating the nature of the exception
                                will be printed, and the function will return to the caller. If an
                                exception occurs and this flag is set to True, a PyCompileError
                                exception will be raised.
                                Defaults to False.
            
            optimize (OptimizationLevel, int, optional): 
                                The optimization level for the compiler.  Valid values
                                are -1, 0, 1 and 2.  A value of -1 means to use the optimization
                                level of the current interpreter, as given by -O command line options.
                                Defaults to Optimization.current_interpreter.
                                
            invalidation_mode (None, optional): 
                                Defaults to None.
                                
            quiet (VerbosityLevel, int, optional): 
                                Return full output with False or 0, errors only with 1,
                                and no output with 2.
                                Defaults to Verbosity.full.

        Raises:
            FileExistsError: File does not exist
        """
        self._file = file
        self._cfile = cfile
        self._dfile = dfile
        self._doraise = doraise
        self._optimize = optimize
        self._invalidation_mode = invalidation_mode
        self._quiet = quiet
        
        
        if self._invalidation_mode is None:
            self._invalidation_mode = _get_default_invalidation_mode()
    
        if self._cfile is None:
            if self._optimize >= 0:
                self._optimization = self._optimize if self._optimize >= 1 else ''
                self._cfile = cache_from_source(self._file, optimization=self._optimization)
            else:
                self._cfile = cache_from_source(self._file)
                
        if os.path.islink(self._cfile):
            self._msg = ('{} is a symlink and will be changed into a regular file if '
                'import writes a byte-compiled file to it')
            raise FileExistsError(self._msg.format(cfile))
        elif os.path.exists(self._cfile) and not os.path.isfile(self._cfile):
            self._msg = ('{} is a non-regular file and will be changed into a regular '
                'one if import writes a byte-compiled file to it')
            raise FileExistsError(self._msg.format(cfile))
        
        self._loader = SourceFileLoader('<py_compile>', file)
        self._source_bytes = self._loader.get_data(file)
        
        try:
            self._code = self._loader.source_to_code(self._source_bytes, self._dfile or self._file, _optimize=optimize)
        except Exception as err:
            self._py_exc = PyCompileError(err.__class__, err, self._dfile or self._file)
            if self._quiet < 2:
                if self._doraise:
                    raise self._py_exc
                else:
                    sys.stderr.write(self._py_exc.msg + '\n')
            return
        
        try:
            self._dirname = os.path.dirname(self._cfile)
            
        except FileExistsError:
            pass
        if self._invalidation_mode == PycInvalidationMode.TIMESTAMP:
            self._source_stats = self._loader.path_stats(self._file)
            self._bytecode = _code_to_timestamp_pyc(self._code, self._source_stats['mtime'], self._source_stats['size'])
        else:
            self._source_hash = source_hash(self._source_bytes)
            self._bytecode = _code_to_hash_pyc(self._code, self._source_hash, (self._invalidation_mode == PycInvalidationMode.CHECKED_HASH), )
            
        self._mode = _calc_mode(file)
        _write_atomic(self._cfile, self._bytecode, self._mode)
        
        self._objects = PythonSourceFile(self._file)
        
        self._object_names = [
            "functions", "classes", 
            "names", "assignments"
        ]
        
        self._object_values = [
            self._objects.functions(), self._objects.classes(), 
            self._objects.names(), self._objects.assignments()
        ]
        
        self.objects = {key:value for key, value in zip(self._object_names, self._object_values)}
        
        self.attribute_values = ( 
            self._file, self._cfile, self._dfile, self._doraise, 
            self._optimize, self._invalidation_mode, self._quiet, 
             self._bytecode, self._code, self._dirname, 
            self._loader, self._mode, 
            self._source_bytes, self._source_stats
        )
        
        self.attribute_names = (
            "file", "cfile", "dfile", "doraise", 
            "optimize", "invalidation_mode", "quiet", 
            "bytecode", "code", "dirname", 
            "loader", "mode",  
            "source_bytes", "source_stats",
        )
        self.Attributes = {key:value for key,value in zip(self.attribute_names, self.attribute_values)}
        self._instructions = dis.Bytecode(self.Attributes["bytecode"]).dis()
    
    def __vars__(self):
        return self.Attributes

    def __dir__(self):
        return self.Attributes
    
    def __getitem__(self, key):
        try:
            return self.Attributes[key]
        except KeyError:
            return None
    
    def __setitem__(self, key, value):
        self.attributes[key] = value
    
    def Bytecode(self):
        return self.Attributes["bytecode"]
    
    def Instructions(self):
        return self._instructions
    
    def show_instructions(self):
        for i in self._instructions:
            print(i)
    
    def SourceCode(self):
        return self._objects.content
    
    def Code(self):
        return self.Attributes["code"]
    
    def Objects(self):
        return self.objects
    
    def bytecode_of(self, value):
        bc = Bytecode(value)
        return [x for x in bc]


class PythonSourceObjects:
    def __init__(self) -> None:
        self._functions = {}
        self._functions_list = []
        self._classes = {}
        self._classes_list = []
        self._names = []
        self._assignments = []
    
    def assignments(self):
        return self._assignments
    
    def names(self):
        return self._names
    
    def functions(self):
        return self._functions
    
    def classes(self):
        return self._classes
    
    def add_function(self, node: ast.FunctionDef):
        self._functions[node.name] = node
        self._functions_list.append(node)
    
    def add_class(self, node: ast.ClassDef):
        self._classes[node.name] = node
        self._functions_list.append(node)
    
    def add_name(self, node: ast.Name):
        self._names.append(node)
    
    def add_assignment(self, node: ast.Assign):
        self._assignments.append(node)


class PythonSourceFile(PythonSourceObjects):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__()
        with open(self.path, "r") as file:
            self.content = file.read()
            self.tree = ast.parse(self.content)
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    self.add_function(node)
                elif isinstance(node, ast.ClassDef):
                    self.add_class(node)
                elif isinstance(node, ast.Assign):
                    self.add_assignment(node)
                    if isinstance(node.targets[0], ast.Name):
                        self.add_name(node)





def test_functions():
    dirname = os.path.join(os.getcwd(), "gui.py")
    pbc = PythonBytecode(dirname)
    print(pbc.Bytecode())
    
test_functions()