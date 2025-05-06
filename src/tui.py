"""
TUI for Strands
"""

import sys
from strands import Strand
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake
from stubs import PosStub, StrandStub, BoardStub, StrandsGameStub
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase


def update_display(strands: StrandsGameBase, connections: list[StrandBase]):
    # Somehow have to also draw connections for shit that has already been found.
    # Once this is done we shld be good
    board: BoardBase = strands.board()
    rows: int = board.num_rows()
    columns: int = board.num_cols()


    print("TOP" + ("-" * (4 * columns)))
    print("TOP" + ("-" * (4 * columns)))
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")

    print("LL" + f" '{strands.theme()}' " + 
          (" " * ((4 * columns) - (5 + len(strands.theme()))) + "RR"))

    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")

    for row in board._letters:
        print("LL ", end = "")
        for elt in row[:-1]:
            print(f"{elt}   ", end = "")
        print(row[-1], end = " ")
        print("RR")
        print("LL" + (" " * ((4 * columns) - 1)) + "RR")

    print("LL " + 
          f"Found {str(len(connections))}/{str(len(strands.answers()))}  Hint 0" 
          + (" " * ((4 * columns) - 19)) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))


def play_game():
    game: StrandsGameBase = StrandsGameStub("filename", hint_threshold = 3)
    board = game.board()
    rows: int = board.num_rows()
    cols: int = board.num_cols()

    found: list[StrandBase] = []

    while not game.game_over():
        update_display(game, found)
        key = input("> ")
        if key == "q":
            break
        if key == "":
            if board.answers == []:
                raise ValueError("Game is already over!")
            ans = board.answers.pop()
            found.append(ans[1])


if __name__ == "__main__":
    play_game()