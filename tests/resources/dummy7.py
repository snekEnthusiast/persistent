from typing import TYPE_CHECKING
if TYPE_CHECKING:
    x: int = 0
import persistent
persistent.config.save_on_exception = True
persistent.init(globals())
persistent.declare(x=1)
print(x)
x+=1
raise Exception