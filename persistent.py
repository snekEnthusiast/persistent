"""
A simple module for persistent data. Before running use, init(globals()) must be called.  When script is changed, run "python3 persisten.py" to clear.
"""
import atexit
from pickle import load,dump
from pathlib import Path
import inspect,shutil,sys

class config:
    "static class for config"
    directory = ".persistent"
    init_with_inspect_stack_hack = False
    def __setattr__(self, name: str, value):
        pass


__namespace:dict = None # type: ignore awaiting namespace set

if config.init_with_inspect_stack_hack:
    __namespace = inspect.stack()[1].frame.f_globals

def init(globals):
    global __namespace
    __namespace = globals

if __name__ == "__main__":
    shutil.rmtree(config.directory)
    sys.exit()
    
__persistents = set([])
#ensure data directory exists
Path(config.directory).mkdir(exist_ok=True)

def __read_variable(name:str):
    f = open(config.directory+"/"+name+".pkl",'rb')
    v = load(f)
    f.close()
    return v

def __save_variable(name:str,var):
    f = open(config.directory+"/"+name+".pkl",'wb')
    dump(var,f)
    f.close()

def declare(**kwargs):
    """
    global persistent variable(s) declaration, name=initial value
    """
    for (name,value) in kwargs.items():
        __persistents.add(name)
        try:
            __namespace[name] = __read_variable(name)
        except:
            __namespace[name] = value

def on_quit():
    for name in __persistents:
        __save_variable(name,__namespace[name])

atexit.register(on_quit)