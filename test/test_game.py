from typing import Tuple, List

import pytest

from src.game import Game
from src.board import Board, Cell
from types_ import Color, Move, Piece


@pytest.mark.parametrize(
    "board, color, dice, expected_moves",
    [
        pytest.param(
            Board.from_dict({0: Cell(1, Color.LIGHT)}),
            Color.LIGHT,
            (5, 3),
            [
                (
                    (Piece(color=Color.LIGHT, position=0), 3),
                    (Piece(color=Color.LIGHT, position=3), 5),
                ),
                (
                    (Piece(color=Color.LIGHT, position=0), 5),
                    (Piece(color=Color.LIGHT, position=5), 3),
                ),
            ],
            id="one piece moves light"
        ),
        pytest.param(
            Board.from_dict({12: Cell(1, Color.DARK)}),
            Color.DARK,
            (5, 3),
            [
                (
                    (Piece(color=Color.DARK, position=12), 5),
                    (Piece(color=Color.DARK, position=17), 3),
                ),
                (
                    (Piece(color=Color.DARK, position=12), 3),
                    (Piece(color=Color.DARK, position=15), 5),
                ),
            ],
            id="one piece moves dark"
        ),
        pytest.param(
            Board.from_dict({0: Cell(1, Color.LIGHT), 3: Cell(1, Color.DARK)}),
            Color.LIGHT,
            (5, 3),
            [
                (
                    (Piece(color=Color.LIGHT, position=0), 5),
                    (Piece(color=Color.LIGHT, position=5), 3)
                )
            ],
            id="dark blocking light",
        ),
        pytest.param(
            Board.from_dict({0: Cell(1, Color.DARK), 3: Cell(1, Color.LIGHT)}),
            Color.DARK,
            (5, 3),
            [
                (
                    (Piece(color=Color.DARK, position=0), 5),
                    (Piece(color=Color.DARK, position=5), 3),
                ),
            ],
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
                (
                    (Piece(color=Color.LIGHT, position=1), 3),
                    (Piece(color=Color.LIGHT, position=4), 5),
                ),
                (
                    (Piece(color=Color.LIGHT, position=1), 5),
                    (Piece(color=Color.LIGHT, position=6), 3),
                ),
                (
                    (Piece(color=Color.LIGHT, position=1), 3),
                    (Piece(color=Color.LIGHT, position=1), 5),
                ),
                (
                    (Piece(color=Color.LIGHT, position=1), 5),
                    (Piece(color=Color.LIGHT, position=1), 3),
                ),
            ],
            id="multiple pieces light"
        ),
        pytest.param(
            Board.from_dict({0: Cell(2, Color.LIGHT)}),
            Color.LIGHT,
            (5, 3),
            [
                (
                        (Piece(color=Color.LIGHT, position=0), 3),
                        (Piece(color=Color.LIGHT, position=3), 5),
                ),
                (
                        (Piece(color=Color.LIGHT, position=0), 5),
                        (Piece(color=Color.LIGHT, position=5), 3),
                ),
            ],
            id="multiple head pieces light"
        ),
        pytest.param(
            Board.from_dict({12: Cell(2, Color.DARK)}),
            Color.DARK,
            (5, 3),
            [
                (
                    (Piece(color=Color.DARK, position=12), 3),
                    (Piece(color=Color.DARK, position=15), 5),
                ),
                (
                    (Piece(color=Color.DARK, position=12), 5),
                    (Piece(color=Color.DARK, position=17), 3),
                ),
            ],
            id="multiple head pieces dark"
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
    actual_moves = [
        tuple((piece.position, step_len) for piece, step_len in move)
        for move in game.find_moves(color, dice)
    ]
    expected_moves = [
        tuple((piece.position, step_len) for piece, step_len in move)
        for move in expected_moves
    ]
    assert sorted(actual_moves) == sorted(expected_moves)

