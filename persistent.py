"""
A simple module for persistent data. Before running use, init(globals()) must be called. Run "python3 persisten.py" and confirm to clear persistent data cache.
Two experimental settings are present:
    stack_auto_init is automatic initialization, will fail if a module loader is present
    hash_antiConflict is a solution to prevent the saved states of variables from different files and their versions from contaminating each other
"""
import atexit
from pickle import load,dump
from pathlib import Path
import inspect,shutil,sys,os,hashlib
import types

class config:
    "static class for config"
    directory = ".persistent"
    stack_auto_init = False
    hash_antiConflict = True
    def __setattr__(self, name: str, value):
        pass

def clear_cache():
    shutil.rmtree(config.directory)

if __name__ == "__main__":
    if sys.argv == ['persistent.py', '-y']:
        clear_cache()
    elif input("Are you sure you want to delete the cache? this action cannot be reversed: (y/n)") == "y":
        clear_cache()
    sys.exit()

#global variables
__namespace:dict = None # type: ignore awaiting namespace set
__subdirectory = "_default"

def __directory():
    return config.directory + "/" + __subdirectory

if config.stack_auto_init:
    "works with the assumption that no module loaders are present"
    __namespace = inspect.stack()[1].frame.f_globals

def _caller_file():
    main = sys.modules.get("__main__")

    if isinstance(main, types.ModuleType):
        path = getattr(main, "__file__", None)
        if path:
            return os.path.abspath(path)

    # Fallback for `python script.py`
    if sys.argv and sys.argv[0]:
        path = sys.argv[0]
        if os.path.isfile(path):
            return os.path.abspath(path)

    return None

def hash_caller(algorithm: str = "sha256") -> tuple[str, str]:
    """Return (hex digest, path) for the script that imported this module."""
    path = _caller_file()

    if not path or not os.path.isfile(path):
        raise RuntimeError("Could not determine the loading script's file")

    hasher = hashlib.new(algorithm)

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)

    return hasher.hexdigest(), path

if config.hash_antiConflict:
    try:
        (digest, path) = hash_caller()
        #print("hash:",digest)
        #print("path",path)
        __subdirectory = digest
    except:
        print("antiConflict Failed!",file=sys.stderr)

def init(globals):
    global __namespace
    __namespace = globals
 
__persistents = set([])
#ensure data directory exists
Path(__directory()).mkdir(exist_ok=True,parents=True)

def __read_variable(name:str):
    f = open(__directory()+"/"+name+".pkl",'rb')
    v = load(f)
    f.close()
    return v

def __save_variable(name:str,var):
    f = open(__directory()+"/"+name+".pkl",'wb+')
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

def __on_quit():
    for name in __persistents:
        __save_variable(name,__namespace[name])

atexit.register(__on_quit)