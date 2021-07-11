from typing import Dict, List

import pytest

from board import Cell, Board
from types_ import Color


@pytest.mark.parametrize(
    "board_state, color, move_length, expected_result",
    [
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                2: Cell(n_pieces=1, color=Color.LIGHT),
            },
            Color.LIGHT,
            3,
            [0, 2],
            id="no blocking"
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                2: Cell(n_pieces=1, color=Color.LIGHT),
                5: Cell(n_pieces=1, color=Color.DARK),
            },
            Color.LIGHT,
            3,
            [0],
            id="blocking"
        )
    ]
)
def test_find_movable_pieces(
    board_state: Dict[int, Cell],
    color: Color,
    move_length: int,
    expected_result: List[int],
):
    board = Board.from_dict(board_state)
    pieces = board.find_movable_pieces(color, move_length)
    assert pieces == expected_result
