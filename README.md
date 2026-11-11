A simple module for data that will persist between sessions. Doesn't support concurrency. Should only be used by scripts in writeable locations.

## Usage
### Initialization
before use initialize the module as follows:
```
import persistent
persistent.init(globals())
```
#### Auto-Initialization
alternatively, set the `config.auto_init` flag to `True` and `persistent.init(globals())` need not be called. The first `declare()` call binds to the globals of the module that called it, so make that call from the module that should own the variables:
```
import persistent
persistent.declare(var=exp)
```
### Persistent Variable
use
```
persistent.declare(var=exp)
```
to create a global persistent variable `var` with the initial value of `exp`. If the program runs correctly and later runs again, the value of `var` will persist through sessions. If the program To cooperate with pylance use
```
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    var: type_of_var = var_type_value
```
otherwise pylance will report undeclared variable `var`
### Settings
currently there are two settings:
	- smart_storage_loaction ensures that a script's persistent data is maintained no matter where it runs and protects from contamination from previous versions. It is turned on by default
	- auto_init allows for auto initialization and is disabled by default. It is considered experimental as issues may occur when using module managers/launchersult.
	- save_on_exception decides whether persistent values are to be saved if the program quits due to an exception exception occurs. Turned off by default
### Deleting Persistent Data
delete `.persistent/<script_name>` folder at the script's location to clear persistent data values.
## Dependencies
Data storage is currently performed by pickle. Any preferred drop-in alternative can be used instead by replacing the import statement.