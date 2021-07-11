from typing import Dict, List

import pytest

from board import Cell, Board
from types_ import Color


@pytest.mark.parametrize(
    "board_state, piece, move_length, expected_result",
    [
        pytest.param(
            {0: Cell(n_pieces=1, color=Color.LIGHT)},
            0,
            3,
            True,
            id="no blocking",
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                5: Cell(n_pieces=1, color=Color.DARK),
            },
            0,
            5,
            False,
            id="blocking",
        ),
        pytest.param(
            {22: Cell(n_pieces=1, color=Color.DARK)},
            22,
            3,
            True,
            id="move dark piece over dark edge",
        ),
        pytest.param(
            {22: Cell(n_pieces=1, color=Color.LIGHT)},
            22,
            3,
            False,
            id="move light piece over dark edge",
        )
    ]
)
def test_can_move_piece(
    board_state: Dict[int, Cell],
    piece: int,
    move_length: int,
    expected_result: bool,
):
    board = Board.from_dict(board_state)
    pieces = board.can_move_piece(piece, move_length)
    assert pieces == expected_result
