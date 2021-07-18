import copy
from typing import Optional, List, Dict, Iterable

from types_ import Color, Cell, Piece

TOTAL_PIECES = 15
NUM_CELLS = 24


def light_cell_order(value: int) -> int:
    return value


def dark_cell_order(value: int) -> int:
    return (value - 12) % 24


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

    def get_piece(self, position: int) -> Optional[Piece]:
        assert 0 <= position <= 23, "unexpected position"

        cell = self._cells[position]

        if cell.n_pieces == 0:
            return None
        else:
            return Piece(color=cell.color, position=position)

    def __copy__(self):
        return Board([copy.copy(cell) for cell in self._cells])

    def can_move_piece(self, piece: Piece, move_length: int) -> bool:
        assert move_length != 0, "0-cell moves are prohibited"
        assert \
            self._cells[piece.position].n_pieces != 0, \
            "provided piece doesn't exist"

        start_cell = self._cells[piece.position]
        target_cell_num = (piece.position + move_length) % NUM_CELLS

        if (
            start_cell.color == Color.LIGHT
            and target_cell_num <= piece.position
        ):
            return False

        target_cell = self._cells[target_cell_num]
        return target_cell.color != start_cell.color.opposite

    def find_movable_pieces(self, color: Color, move_length: int) -> Iterable[Piece]:
        return [
            Piece(color=color, position=i)
            for i, cell in enumerate(self._cells)
            if (
                cell.color == color
                and self._cells[i + move_length].color != color.opposite
            )
        ]

    def move_piece(self, piece: Piece, move_length: int):
        assert 0 < move_length <= 6, "Invalid move length"

        start_cell = self._cells[piece.position]
        assert start_cell.n_pieces != 0, "Attempt to move from empty cell"

        end_cell = self._cells[piece.position + move_length]
        assert \
            end_cell.color != start_cell.color.opposite, \
            "Attempt to step to opposite color"

        move_color = start_cell.color

        start_cell.n_pieces -= 1
        if start_cell.n_pieces == 0:
            start_cell.color = None

        end_cell.n_pieces += 1
        end_cell.color = move_color

    def get_last_piece(self, color: Color) -> Optional[Piece]:
        key = light_cell_order if color == Color.LIGHT else dark_cell_order

        appropriate_cells = [
            i for i, cell in enumerate(self._cells) if cell.color == color
        ]

        if len(appropriate_cells) == 0:
            return None

        last_position = min(appropriate_cells, key=key)
        return Piece(color=color, position=last_position)