from typing import TYPE_CHECKING
if TYPE_CHECKING:
    x: int = 0
import persistent
persistent.init(globals())
persistent.declare(x=0)
x+=2
print(x)