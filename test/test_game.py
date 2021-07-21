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
        pytest.param(
            Board.from_dict({
                0: Cell(1, Color.LIGHT),
                8: Cell(1, Color.DARK),
            }),
            Color.LIGHT,
            (5, 3),
            [
                ((Piece(color=Color.LIGHT, position=0), 3),),
                ((Piece(color=Color.LIGHT, position=0), 5),),
            ],
            id="light: partial moves",
        ),
        pytest.param(
            Board.from_dict({
                0: Cell(1, Color.LIGHT),
                1: Cell(1, Color.LIGHT),
                8: Cell(1, Color.DARK),
            }),
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
                    (Piece(color=Color.LIGHT, position=0), 3),
                    (Piece(color=Color.LIGHT, position=1), 5),
                ),
                (
                    (Piece(color=Color.LIGHT, position=1), 5),
                    (Piece(color=Color.LIGHT, position=0), 3),
                ),
                (
                    (Piece(color=Color.LIGHT, position=0), 5),
                    (Piece(color=Color.LIGHT, position=1), 3),
                ),
                (
                    (Piece(color=Color.LIGHT, position=1), 3),
                    (Piece(color=Color.LIGHT, position=0), 5),
                ),
            ],
            id="light: partial and full moves",
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


@pytest.mark.parametrize(
    "board, color, expected_result",
    [
        pytest.param(
            Board.from_dict({}),
            Color.LIGHT,
            False,
            id="light: no pieces"
        ),
        pytest.param(
            Board.from_dict({
                0: Cell(n_pieces=4, color=Color.LIGHT),
                6: Cell(n_pieces=3, color=Color.LIGHT),
                12: Cell(n_pieces=8, color=Color.LIGHT),
            }),
            Color.LIGHT,
            False,
            id="light: all pieces outside of home"
        ),
        pytest.param(
            Board.from_dict({
                17: Cell(n_pieces=4, color=Color.LIGHT),
                18: Cell(n_pieces=3, color=Color.LIGHT),
                22: Cell(n_pieces=8, color=Color.LIGHT),
            }),
            Color.LIGHT,
            False,
            id="light: some pieces are home"
        ),
        pytest.param(
            Board.from_dict({
                0: Cell(n_pieces=4, color=Color.LIGHT),
                5: Cell(n_pieces=3, color=Color.DARK),
                16: Cell(n_pieces=3, color=Color.LIGHT),
                20: Cell(n_pieces=2, color=Color.DARK),
                22: Cell(n_pieces=8, color=Color.LIGHT),
            }),
            Color.LIGHT,
            False,
            id="light: some pieces are home some dark mixed in"
        ),
        pytest.param(
            Board.from_dict({
                18: Cell(n_pieces=4, color=Color.LIGHT),
                21: Cell(n_pieces=3, color=Color.LIGHT),
                22: Cell(n_pieces=8, color=Color.LIGHT),
            }),
            Color.LIGHT,
            True,
            id="light: all pieces home"
        ),
        pytest.param(
            Board.from_dict({
                5: Cell(n_pieces=3, color=Color.DARK),
                18: Cell(n_pieces=4, color=Color.LIGHT),
                19: Cell(n_pieces=1, color=Color.DARK),
                21: Cell(n_pieces=3, color=Color.LIGHT),
                22: Cell(n_pieces=8, color=Color.LIGHT),
            }),
            Color.LIGHT,
            True,
            id="light: all pieces home dark mixed in"
        ),
        pytest.param(
            Board.from_dict({}),
            Color.DARK,
            False,
            id="dark: no pieces"
        ),
        pytest.param(
            Board.from_dict({
                0: Cell(n_pieces=4, color=Color.DARK),
                5: Cell(n_pieces=3, color=Color.DARK),
                12: Cell(n_pieces=8, color=Color.DARK),
                23: Cell(n_pieces=3, color=Color.DARK),
            }),
            Color.DARK,
            False,
            id="dark: all pieces outside of home"
        ),
        pytest.param(
            Board.from_dict({
                2: Cell(n_pieces=4, color=Color.DARK),
                6: Cell(n_pieces=3, color=Color.DARK),
                11: Cell(n_pieces=2, color=Color.DARK),
                13: Cell(n_pieces=5, color=Color.DARK),
            }),
            Color.DARK,
            False,
            id="dark: some pieces are home"
        ),
        pytest.param(
            Board.from_dict({
                2: Cell(n_pieces=4, color=Color.DARK),
                6: Cell(n_pieces=3, color=Color.DARK),
                8: Cell(n_pieces=2, color=Color.LIGHT),
                10: Cell(n_pieces=4, color=Color.LIGHT),
                11: Cell(n_pieces=2, color=Color.DARK),
                13: Cell(n_pieces=5, color=Color.DARK),
            }),
            Color.DARK,
            False,
            id="dark: some pieces are home some light mixed in"
        ),
        pytest.param(
            Board.from_dict({
                6: Cell(n_pieces=4, color=Color.DARK),
                7: Cell(n_pieces=3, color=Color.DARK),
                11: Cell(n_pieces=8, color=Color.DARK),
            }),
            Color.DARK,
            True,
            id="dark: all pieces home"
        ),
        pytest.param(
            Board.from_dict({
                2: Cell(n_pieces=2, color=Color.LIGHT),
                6: Cell(n_pieces=4, color=Color.DARK),
                7: Cell(n_pieces=3, color=Color.DARK),
                10: Cell(n_pieces=1, color=Color.LIGHT),
                11: Cell(n_pieces=8, color=Color.DARK),
            }),
            Color.DARK,
            True,
            id="dark: all pieces home dark mixed in"
        ),
    ]
)
def test_is_home(
    board: Board,
    color: Color,
    expected_result: bool,
):
    game = Game(board)
    result = game.is_home(color)
    assert result == expected_result
