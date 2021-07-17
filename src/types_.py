from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional


class Color(Enum):
    LIGHT = 1
    DARK = 2

    @property
    def opposite(self) -> "Color":
        if self == Color.LIGHT:
            return Color.DARK
        else:
            return Color.LIGHT


@dataclass
class Piece:
    color: Color
    position: int


CellNum = int
StepLen = int
Step = Tuple[Piece, StepLen]
Move = Tuple[Step, ...]


@dataclass
class Cell:
    n_pieces: int = 0
    color: Optional[Color] = None
