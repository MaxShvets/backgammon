from typing import Tuple, List

import pytest

from src.game import Game
from src.board import Board, Cell
from types_ import Color, Move


@pytest.mark.parametrize(
    "board, color, dice, expected_moves",
    [
        pytest.param(
            Board.from_dict({0: Cell(1, Color.LIGHT)}),
            Color.LIGHT,
            (5, 3),
            [((0, 3), (3, 5)), ((0, 5), (5, 3))],
            id="one piece moves light"
        ),
        pytest.param(
            Board.from_dict({12: Cell(1, Color.DARK)}),
            Color.DARK,
            (5, 3),
            [((12, 5), (17, 3)), ((12, 3), (15, 5))],
            id="one piece moves dark"
        ),
        pytest.param(
            Board.from_dict({0: Cell(1, Color.LIGHT), 3: Cell(1, Color.DARK)}),
            Color.LIGHT,
            (5, 3),
            [((0, 5), (5, 3))],
            id="dark blocking light",
        ),
        pytest.param(
            Board.from_dict({0: Cell(1, Color.DARK), 3: Cell(1, Color.LIGHT)}),
            Color.DARK,
            (5, 3),
            [((0, 5), (5, 3))],
            id="light blocking dark",
        ),
        pytest.param(
            Board.from_dict({
                0: Cell(1, Color.LIGHT),
                3: Cell(1, Color.DARK),
                5: Cell(1, Color.DARK),
            }),
            Color.LIGHT,
            (5, 3),
            [],
            id="no moves",
        ),
        pytest.param(
            Board.from_dict({1: Cell(2, Color.LIGHT)}),
            Color.LIGHT,
            (5, 3),
            [
                ((1, 3), (4, 5)),
                ((1, 5), (6, 3)),
                ((1, 3), (1, 5)),
                ((1, 5), (1, 3)),
            ],
            id="multiple pieces light"
        ),
    ]
)
def test_find_moves(
    board: Board,
    color: Color,
    dice: Tuple[int, int],
    expected_moves: List[Move]
):
    game = Game(board)
    assert sorted(game.find_moves(color, dice)) == sorted(expected_moves)

