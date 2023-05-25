import dis
import os 
from lib import CompileMode, FileMode
import tabulate



    

def get_bytecode_instructions(file_path: str) -> list[str]:
    """ accepts a path of a Python file as a string and 
    returns the bytecode instructions as a list of strings

    Args:
        file_path (str): string path to the file

    Returns:
        list[str]: string list of bytecode instructions
    """
    if file_path.endswith(".py") and os.path.exists(file_path):
        with open(file_path, FileMode.read) as f:
            source = f.read()
        fn = os.path.basename(file_path)
        try:
            bytecode = dis.Bytecode(
                compile(source, filename='<string>', mode=CompileMode.execute)
            )
            
            lns = [[str(cell).ljust(25).strip() for cell in x] for x in bytecode]
            #table = tabulate.tabulate(lns, colalign='left', tablefmt="rounded_grid", stralign='left', numalign='left')
            return lns
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("Error reading file.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")