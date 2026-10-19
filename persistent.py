"""
A simple module for persistent data. When script is changed, run "python3 persisten.py" to clear
"""
import atexit
from pickle import load,dump
from pathlib import Path

directory = ".persistent"
namespace:dict = None # type: ignore awaiting namespace set

def init(globals):
    global namespace
    namespace = globals

if __name__ == "__main__":
    import shutil
    shutil.rmtree(directory)
    import sys
    sys.exit()
    
__persistents = set([])
#ensure data directory exists
Path(directory).mkdir(exist_ok=True)

def __read_variable(name:str):
    f = open(directory+"/"+name+".pkl",'rb')
    v = load(f)
    f.close()
    return v

def __save_variable(name:str,var):
    f = open(directory+"/"+name+".pkl",'wb')
    dump(var,f)
    f.close()

def declare(**kwargs):
    """
    global persistent variable(s) declaration, name=initial value
    """
    for (name,value) in kwargs.items():
        __persistents.add(name)
        try:
            namespace[name] = __read_variable(name)
        except:
            namespace[name] = value

def on_quit():
    for name in __persistents:
        __save_variable(name,namespace[name])

atexit.register(on_quit)