from enum import Enum
from typing import Tuple

CellNum = int
StepLen = int
Step = Tuple[CellNum, StepLen]
Move = Tuple[Step, ...]


class Color(Enum):
    LIGHT = 1
    DARK = 2

    @property
    def opposite(self) -> "Color":
        if self == Color.LIGHT:
            return Color.DARK
        else:
            return Color.LIGHT
