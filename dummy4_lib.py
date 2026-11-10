from typing import TYPE_CHECKING
if TYPE_CHECKING:
    libvar: int = 0
import persistent
persistent.declare(libvar=100)
