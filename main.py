from pprint import pprint

from src.board import Board, Color


def main():
    board = Board()
    pprint(board.find_moves(Color.LIGHT, (1, 2)))


if __name__ == "__main__":
    main()
