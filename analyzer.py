from collections.abc import Mapping
from importlib.util import decode_source
from importlib.util import cache_from_source, source_from_cache, source_hash
from importlib.resources import read_binary, read_text 
from types import ModuleType, FunctionType, MethodType, ClassMethodDescriptorType, DynamicClassAttribute, CoroutineType, CodeType
from types import coroutine, GeneratorType
from dis import Bytecode
import dis
import py_compile
import os
import sys
import code
from typing import Any, Sequence
import codeop


class Local:
    default = {"__name__": '__console__','__doc__':None }


class PythonConsole(code.InteractiveConsole):
    def __init__(self, locals: Mapping[str, Any] | None = None, filename: str = "<console>") -> None:
        super().__init__(locals, filename)
        


def interactive_interpreter(locals=None) -> code.InteractiveInterpreter:
    """
    This class deals with parsing and interpreter state (the users namespace); 
    it does not deal with input buffering or prompting or input file naming 
    (the filename is always passed in explicitly).
     
    Args:
        locals (_type_, optional): 
                The optional locals argument specifies the dictionary in 
                which code will be executed. Defaults to None.

    Returns:
        code.InteractiveInterpreter: interactive interpreter class
    """
    return code.InteractiveInterpreter(locals=locals)

def interactive_console(locals=None, filename='<console>') -> code.InteractiveConsole:
    """Closely emulate the behavior of the interactive Python interpreter. 
    This class builds on InteractiveInterpreter and adds prompting using 
    the familiar sys.ps1 and sys.ps2, and input buffering.

    Args:
        locals (_type_, optional): 
                The optional locals argument specifies the dictionary in 
                which code will be executed. Defaults to None.. Defaults to None.
                
        filename (str, optional): 
                filename. Defaults to '<console>'.

    Returns:
        code.InteractiveConsole
    """
    return code.InteractiveConsole(locals=locals, filename=filename)

def interact(banner=None, readfunc=None, local=None, exitmsg=None) -> None:
    """Convenience function to run a read-eval-print loop. 
    This creates a new instance of InteractiveConsole and 
    sets readfunc to be used as the InteractiveConsole.raw_input() method, 
    if provided. If local is provided, it is passed to the InteractiveConsole 
    constructor for use as the default namespace for the interpreter loop. 
    The interact() method of the instance is then run with banner and exitmsg 
    passed as the banner and exit message to use, if provided. 
    The console object is discarded after use.

    Args:
        banner (_type_, optional): _description_. Defaults to None.
        readfunc (_type_, optional): _description_. Defaults to None.
        local (_type_, optional): _description_. Defaults to None.
        exitmsg (_type_, optional): _description_. Defaults to None.
    """
    code.interact(banner=banner, readfunc=readfunc, local=local, exitmsg=exitmsg)

def compile_code(source: str, filename: str='<input>', symbol: str='single') -> CodeType|None:
    """This function is useful for programs that want to emulate 
    Python’s interpreter main loop (a.k.a. the read-eval-print loop).
     
    The tricky part is to determine when the user has entered an incomplete 
    command that can be completed by entering more text (as opposed to a complete command or a syntax error). 
    This function almost always makes the same decision as the real interpreter main loop.

    Args:
        source (str):  source string
        filename (str, optional): optional filename from which source was read. Defaults to '<input>'.
        symbol (str, optional): _description_. Defaults to 'single'.

    Returns:
        CodeType|None: CodeType if valid None if invalid
    """
    code.compile_command(source, filename, symbol)

def run_code(_code):
    code.InteractiveInterpreter.runcode(_code)


#================================================================
# MODULE STUFF
#================================================================

def get_module(string: str) -> ModuleType:
    return __import__(string)

#================================================================
# Coroutine Stuff
#================================================================
def generator_to_coroutine(generator: GeneratorType) -> CoroutineType:
    return coroutine(generator)    


#================================================================
# Function Stuff
#================================================================

def get_function(module: str, function: str) -> FunctionType:
    """ Get a function by string module name and string function name """
    imp = __import__(module)
    return getattr(imp, function)


#================================================================
# Bytecode Stuff
#================================================================
def filepath_to_bytecode(filepath: str) -> Bytecode:
    pass


#================================================================
# Version Stuff
#================================================================

def get_python_version_information() -> str:
    return sys.version

def get_python_version() -> str:
    return get_python_version_information().split(" ")[0]

def get_python_major_version() -> str:
    return get_python_version().split(".")[1]

def get_python_minor_version() -> str:
    return get_python_version().split(".")[2]

def get_python_cache_version() -> str:
    return "".join(get_python_version().split(".")[:-1])

#================================================================
# Path Stuff
#================================================================

def path_to_cache_path(path: str) -> str:
    """
    takes a python filepath and returns where the cache would be stored 
    """
    cachename = os.path.basename(path).split(".")[0] + ".cpython-" + get_python_cache_version() + ".pyc"
    return os.path.join(path, '__pycache__', cachename)
    

#================================================================
# Compile Stuff
#================================================================

def compile_python_file(filepath: str) -> str:
    """ Takes a filepath and return the cache path
    """
    if os.path.exists(filepath):
        try:
            py_compile.compile(filepath)
        except py_compile.PyCompileError as e:
            return e
        finally:
            return path_to_cache_path(filepath)

def create_function_dictionary():
    function_dict = {}
    global_objects = globals()

    for name, obj in global_objects.items():
        if callable(obj) and hasattr(obj, '__name__'):
            function_dict[name] = obj

    return function_dict

def dissemble_function(function_name: str, module=None) -> str|None:
    func = None
    if module == None:
        for name, function in create_function_dictionary().items():
            if name == function_name:
                func = function
                break
    else:
        mod = __import__(module)
        func = getattr(mod, function_name)
    code = dis.Bytecode(func)
    lines = code.dis()
    
    print(lines)

dissemble_function('compile_python_file')


    
    