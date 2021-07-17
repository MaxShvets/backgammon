import copy
from typing import Tuple, List, Iterable

from board import Board
from types_ import Color, Move, Piece


class Game:
    def __init__(self, board: Board):
        self._board = board

    @staticmethod
    def is_head_piece(piece: Piece):
        return (
            (piece.color == Color.LIGHT and piece.position == 0)
            or (piece.color == Color.DARK and piece.position == 12)
        )

    def _find_step_sequence(
        self, color: Color, seq: Iterable[int]
    ) -> List[Move]:
        moves: List[Tuple[Move, Board, bool]] = [((), self._board, False)]

        for step_len in seq:
            extended_moves = []

            for move, board, was_head_move_made in moves:
                pieces = board.find_movable_pieces(color, step_len)

                for piece in pieces:
                    is_head_move = self.is_head_piece(piece)
                    if was_head_move_made and is_head_move:
                        continue

                    step = (piece, step_len)
                    updated_board = copy.copy(board)
                    updated_board.move_piece(*step)
                    extended_move = move + (step,)
                    extended_moves.append(
                        (
                            extended_move,
                            updated_board,
                            was_head_move_made or is_head_move,
                        )
                    )

            moves = extended_moves

        return [move for move, _, __ in moves]

    def find_moves(self, color: Color, dice: Tuple[int, int]) -> List[Move]:
        return (
            self._find_step_sequence(color, dice)
            + self._find_step_sequence(color, reversed(dice))
        )