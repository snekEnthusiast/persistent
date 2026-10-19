A simple module for data that will persist between sessions. Non-parallel

## Usage
### Initialization
before use initialize the module as follows:
```
import persistent
persistent.init(globals())
```
#### Auto-Initialization
alternatively, the `config.init_with_inspect_stack_hack` flag can be set to True and `persistent.init(globals())` need not be called, but this is brittle and may not work as intended
### Persistent Variable
use
```
persistent.declare(var=exp)
```
to create a global persistent variable `var` with the initial value of `exp`. If the program is closed correctly and later runs again, the value of `var` will persist through sessions.
### On script change
run `python3 persistent.py` to clear persistent data cache and avoid contamination from previus script version
## Dependencies
Data storage is currently performed by pickle. Any preferred drop-in alternative can be used instead by replacing the import statement.