import copy
from typing import Tuple, List, Iterable

from board import Board
from types_ import Color, Move


class Game:
    def __init__(self, board: Board):
        self._board = board

    def _find_step_sequence(
        self, color: Color, seq: Iterable[int]
    ) -> List[Move]:
        moves: List[Tuple[Move, Board]] = [((), self._board)]

        for step_len in seq:
            extended_moves = []

            for move, board in moves:
                pieces = board.find_movable_pieces(color, step_len)

                for piece in pieces:
                    step = (piece, step_len)
                    updated_board = copy.copy(board)
                    updated_board.move_piece(*step)
                    extended_move = move + (step,)
                    extended_moves.append((extended_move, updated_board))

            moves = extended_moves

        return [move for move, _ in moves]

    def find_moves(self, color: Color, dice: Tuple[int, int]) -> List[Move]:
        return (
            self._find_step_sequence(color, dice)
            + self._find_step_sequence(color, reversed(dice))
        )