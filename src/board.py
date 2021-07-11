import copy
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, List, Iterable, Dict

TOTAL_PIECES = 15

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


@dataclass
class Cell:
    n_pieces: int = 0
    color: Optional[Color] = None


class Board:
    def __init__(self, cells: Optional[List[Cell]] = None):
        if cells:
            self._cells = cells
        else:
            self._cells = [Cell() for _ in range(24)]

            light_start_cell = self._cells[0]
            light_start_cell.color = Color.LIGHT
            light_start_cell.n_pieces = TOTAL_PIECES

            dark_start_cell = self._cells[12]
            dark_start_cell.color = Color.DARK
            dark_start_cell.n_pieces = TOTAL_PIECES

    @classmethod
    def from_dict(cls, board_state: Dict[int, Cell]) -> "Board":
        return cls(cells=[board_state.get(i, Cell()) for i in range(24)])

    def __copy__(self):
        return Board([copy.copy(cell) for cell in self._cells])

    def find_steps(
        self, color: Color, length: int
    ) -> List[Step]:
        steps = []

        for i, cell in enumerate(self._cells):
            if (
                cell.color == color
                and self._cells[i + length].color != color.opposite
            ):
                steps.append((i, length))

        return steps

    def step(self, step: Step):
        cell_num, length = step

        assert 0 < length <= 6, "Invalid step length"

        start_cell = self._cells[cell_num]
        assert start_cell.n_pieces != 0, "Attempt to step from empty cell"

        end_cell = self._cells[cell_num + length]
        assert \
            end_cell.color != start_cell.color.opposite, \
            "Attempt to step to opposite color"

        step_color = start_cell.color

        start_cell.n_pieces -= 1
        if start_cell.n_pieces == 0:
            start_cell.color = None

        end_cell.n_pieces += 1
        end_cell.color = step_color

    def _find_step_sequence(
        self, color: Color, seq: Iterable[int]
    ) -> List[Move]:
        moves: List[Tuple[Move, Board]] = [((), self)]

        for step_len in seq:
            extended_moves = []

            for move, board in moves:
                steps = board.find_steps(color, step_len)

                for step in steps:
                    updated_board = copy.copy(board)
                    updated_board.step(step)
                    extended_move = move + (step,)
                    extended_moves.append((extended_move, updated_board))

            moves = extended_moves

        return [move for move, _ in moves]

    def find_moves(self, color: Color, dice: Tuple[int, int]) -> List[Move]:
        return (
            self._find_step_sequence(color, dice)
            + self._find_step_sequence(color, reversed(dice))
        )
