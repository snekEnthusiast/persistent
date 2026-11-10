from typing import TYPE_CHECKING
if TYPE_CHECKING:
    x: int = 0
import persistent
persistent.config.auto_init = True
import dummy4_lib # declares its own variable before main does
persistent.declare(x=0)
x+=1
dummy4_lib.libvar+=1
print(x, dummy4_lib.libvar, 'x' in vars(dummy4_lib))
