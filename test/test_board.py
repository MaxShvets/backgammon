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
            id="free target cell",
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                5: Cell(n_pieces=1, color=Color.LIGHT),
            },
            0,
            5,
            True,
            id="target cell taken up by the same color",
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                5: Cell(n_pieces=1, color=Color.DARK),
            },
            0,
            5,
            False,
            id="target cell taken up by the opposite color",
        ),
        pytest.param(
            {22: Cell(n_pieces=1, color=Color.DARK)},
            22,
            3,
            True,
            id="move dark piece over dark edge to a free cell",
        ),
        pytest.param(
            {
                22: Cell(n_pieces=1, color=Color.DARK),
                1: Cell(n_pieces=1, color=Color.LIGHT),
            },
            22,
            3,
            False,
            id=(
                "move dark piece over dark edge to "
                "a cell taken by the opposite color piece"
            ),
        ),
        pytest.param(
            {
                22: Cell(n_pieces=1, color=Color.DARK),
                1: Cell(n_pieces=1, color=Color.DARK),
            },
            22,
            3,
            True,
            id=(
                "move dark piece over dark edge to "
                "a cell taken by the same color piece"
            ),
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
            id="light moves, only light pieces"
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.LIGHT),
                2: Cell(n_pieces=1, color=Color.LIGHT),
                6: Cell(n_pieces=1, color=Color.DARK),
            },
            Color.LIGHT,
            3,
            [0, 2],
            id="light moves, dark pieces present"
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
            id="light moves, dark pieces present and block light pieces"
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.DARK),
                2: Cell(n_pieces=1, color=Color.DARK),
            },
            Color.DARK,
            3,
            [0, 2],
            id="dark moves, only dark pieces"
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.DARK),
                2: Cell(n_pieces=1, color=Color.DARK),
                5: Cell(n_pieces=1, color=Color.LIGHT),
            },
            Color.DARK,
            3,
            [0],
            id="dark moves, light pieces present"
        ),
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
