import persistent
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    x: int = 0
persistent.init(globals())
persistent.declare(x=0)
x += 1
print(x)