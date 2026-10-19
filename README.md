A simple module for data that will persist between sessions. Non-parallel

## Usage
#### Initialization
```
import persistent
persistent.init(globals())
```
#### Persistent Variable
use
```
persistent.declare(var=exp)
```
to create a global persistent variable `var` with the initial value of `exp`. If the program is closed correctly and later runs again, the value of `var` will persist through sessions.
#### On script change
run `python3 persistent.py` to clear persistent data cache
## Dependencies
Data storage is currently performed by pickle. Any preferred drop-in alternative can be used instead by replacing the import statement.