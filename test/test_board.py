from typing import Dict, List, Optional

import pytest

from board import Cell, Board
from types_ import Color, Piece


@pytest.mark.parametrize(
    "board_state, position, move_length, expected_result",
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
        ),
    ]
)
def test_can_move_piece(
    board_state: Dict[int, Cell],
    position: int,
    move_length: int,
    expected_result: bool,
):
    board = Board.from_dict(board_state)
    piece = board.get_piece(position)
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
            [
                Piece(color=Color.LIGHT, position=0),
                Piece(color=Color.LIGHT, position=2),
            ],
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
            [
                Piece(color=Color.LIGHT, position=0),
                Piece(color=Color.LIGHT, position=2),
            ],
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
            [Piece(color=Color.LIGHT, position=0)],
            id="light moves, dark pieces present and block light pieces"
        ),
        pytest.param(
            {
                0: Cell(n_pieces=1, color=Color.DARK),
                2: Cell(n_pieces=1, color=Color.DARK),
            },
            Color.DARK,
            3,
            [
                Piece(color=Color.DARK, position=0),
                Piece(color=Color.DARK, position=2),
            ],
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
            [Piece(color=Color.DARK, position=0)],
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


@pytest.mark.parametrize(
    "board_state, color, expected_piece",
    [
        pytest.param({}, Color.LIGHT, None, id="empty board light"),
        pytest.param(
            {2: Cell(n_pieces=1, color=Color.LIGHT)},
            Color.LIGHT,
            Piece(color=Color.LIGHT, position=2),
            id="one piece light"
        ),
        pytest.param(
            {
                2: Cell(n_pieces=1, color=Color.LIGHT),
                4: Cell(n_pieces=2, color=Color.LIGHT),
            },
            Color.LIGHT,
            Piece(color=Color.LIGHT, position=2),
            id="multiple light pieces light"
        ),
        pytest.param(
            {
                1: Cell(n_pieces=2, color=Color.DARK),
                2: Cell(n_pieces=1, color=Color.LIGHT),
                4: Cell(n_pieces=2, color=Color.LIGHT),
                7: Cell(n_pieces=1, color=Color.DARK),
            },
            Color.LIGHT,
            Piece(color=Color.LIGHT, position=2),
            id="multiple mixed pieces light"
        ),
        pytest.param({}, Color.DARK, None, id="empty board dark"),
        pytest.param(
            {2: Cell(n_pieces=1, color=Color.DARK)},
            Color.DARK,
            Piece(color=Color.DARK, position=2),
            id="one piece dark"
        ),
        pytest.param(
            {
                2: Cell(n_pieces=1, color=Color.DARK),
                4: Cell(n_pieces=2, color=Color.DARK),
            },
            Color.DARK,
            Piece(color=Color.DARK, position=2),
            id="multiple light pieces dark"
        ),
        pytest.param(
            {
                1: Cell(n_pieces=2, color=Color.DARK),
                2: Cell(n_pieces=1, color=Color.LIGHT),
                4: Cell(n_pieces=2, color=Color.LIGHT),
                7: Cell(n_pieces=1, color=Color.DARK),
                13: Cell(n_pieces=2, color=Color.DARK),
            },
            Color.DARK,
            Piece(color=Color.DARK, position=13),
            id="multiple mixed pieces dark"
        ),
    ]
)
def test_get_last_piece(
    board_state: Dict[int, Cell],
    color: Color,
    expected_piece: Piece,
):
    board = Board.from_dict(board_state)
    actual_piece = board.get_last_piece(color)
    assert actual_piece == expected_piece


@pytest.mark.parametrize(
    "position, expected_piece",
    [
        pytest.param(0, None, id="no piece"),
        pytest.param(
            2,
            Piece(color=Color.LIGHT, position=2),
            id="no piece"
        ),
        pytest.param(
            4,
            Piece(color=Color.DARK, position=4),
            id="no piece"
        )
    ]
)
def test_get_top_piece(
    position: int,
    expected_piece: Optional[Piece],
):
    board = Board.from_dict({
        2: Cell(n_pieces=2, color=Color.LIGHT),
        4: Cell(n_pieces=4, color=Color.DARK),
    })
    piece = board.get_piece(position)
    assert piece == expected_piece
