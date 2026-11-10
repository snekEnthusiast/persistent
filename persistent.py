"""
A simple module for persistent data. Before running use, init(globals()) must be called. Delete the .persistent folder to clear persistent data cache. This module is supposed to work on picklable data and be run multiple times, with the assumption that it worked correctly before.
Settings Present:
    smart_storage_loaction: will store the persistent values at main script's location and separate them by script & version. Turned on by default
Experimental settings present:
    auto_init is automatic initialization: each declare() call binds its variables to its own caller's globals (used only when init() was not called). Set it after importing, before the first declare()
"""
import atexit
from pickle import load,dump,dumps
from pathlib import Path
import shutil,sys,os,hashlib
import types
import fcntl
from contextlib import contextmanager

class config:
    "static class for config"
    directory = ".persistent"
    auto_init = False
    smart_storage_loaction = True
    def __setattr__(self, name: str, value):
        pass

if __name__ == "__main__":
    sys.exit()

#global variables
__namespace:dict = None # type: ignore awaiting namespace set
__subdirectory = "_default"
__script_directory = ""

def __directory():
    return __script_directory + config.directory + "/" + __subdirectory

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
    hasher.update(path.encode('utf-8'))

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)

    return hasher.hexdigest(), path

if config.smart_storage_loaction:
    try:
        (digest, path) = hash_caller()
        #print("hash:",digest)
        #print("path",path)
        __subdirectory = digest
        __script_directory = '/'.join(path.split('/')[:-1]) + "/"
    except:
        print("smart_storage_loaction Failed!",file=sys.stderr)

def init(globals):
    global __namespace
    __namespace = globals
 
__persistents: dict = {} # name -> namespace the variable lives in
#ensure data directory exists
Path(__directory()).mkdir(exist_ok=True,parents=True)

@contextmanager
def __locked(exclusive: bool):
    """
    Hold a Linux advisory lock (flock) over this script's own .persistent/<hash> directory.
    Shared for reading, exclusive for writing, so concurrently running instances of the
    same script never see half-written files, while different scripts don't block each other.
    """
    fd = os.open(__directory() + "/.lock", os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        yield
    finally:
        os.close(fd) # closing the descriptor releases the lock

def __read_variable(name:str):
    f = open(__directory()+"/"+name+".pkl",'rb')
    v = load(f)
    f.close()
    return v

def __save_variable(name:str,var):
    #check picklability before opening file
    dumps(var)
    f = open(__directory()+"/"+name+".pkl",'wb+')
    dump(var,f)
    f.close()

def declare(**kwargs):
    """
    global persistent variable(s) declaration, name=initial value
    """
    namespace = __namespace
    if namespace is None and config.auto_init:
        # resolve per call, so each declaring module gets its own variables
        namespace = sys._getframe(1).f_globals
    with __locked(exclusive=False):
        for (name,value) in kwargs.items():
            __persistents[name] = namespace
            try:
                namespace[name] = __read_variable(name)
            except:
                namespace[name] = value

def __on_quit():
    if not __persistents:
        return
    with __locked(exclusive=True):
        for (name,namespace) in __persistents.items():
            try:
                __save_variable(name,namespace[name])
            except:
                print("problems with pickling " +name +"!",file=sys.stderr)

atexit.register(__on_quit)