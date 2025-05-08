"""
TUI for Strands
"""

import sys
from strands import Strand
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake
from stubs import PosStub, StrandStub, BoardStub, StrandsGameStub
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase


def update_display(strands: StrandsGameBase, connections: list[StrandBase]):
    board: BoardBase = strands.board()
    rows: int = board.num_rows()
    columns: int = board.num_cols()
    bold: str = "\033[1m"
    reset: str = "\033[0m"
    blue: str = "\033[34m"

    horiz: set[tuple[int, tuple[int, int]]] = set()
    vert: set[tuple[int, tuple[int, int]]] = set()
    diag_slash: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    diag_backslash: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for strand in connections:
        positions: list[PosBase] = strand.positions()
        for i, _ in enumerate(positions[:-1]):
            p1: int = positions[i]
            p2: int = positions[i+1]
            r1: int
            c1: int
            r1, c1 = p1.r, p1.c
            r2: int
            c2: int
            r2, c2 = p2.r, p2.c
            dr: int
            dc: int
            dr = r2 - r1
            dc = c2 - c1
            if dr == 0:
                horiz.add((r1, min(c1, c2)))
            elif dc == 0:
                vert.add((min(r1, r2), c1))
            else:
                if (dr, dc) == (1, 1) or (dr, dc) == (-1, -1):
                    diag_backslash.add((min(r1, r2), min(c1, c2)))
                else:
                    diag_slash.add((min(r1, r2), min(c1, c2)))

    found_pos: list[tuple[int, int]] = []
    for strand in connections:
        for p in strand.positions():
            coord = (p.r, p.c)
            if coord not in found_pos:
                found_pos.append(coord)

    print("TOP" + ("-" * (4 * columns)))
    print("TOP" + ("-" * (4 * columns)))
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")

    print("LL" + f" '{strands.theme()}' " + 
          (" " * ((4 * columns) - (5 + len(strands.theme()))) + "RR"))

    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")

    for r in range(rows):
        print("LL ", end = "")
        for c in range(columns):
            letter = board.get_letter(Pos(r, c))
            display: str
            if (r, c) in found_pos:
                display = bold + blue + letter + reset
            else:
                display = letter
            if c < columns - 1:
                if (r, c) in horiz:
                    print(display + " - ", end = "")
                else:
                    print(display + "   ", end = "")
            else:
                print(display + " ", end = "")
        print("RR")
        between_rows: list[str] = []
        for _ in range(4 * columns - 2):
            between_rows.append(" ")
        if r < rows - 1:
            for coord in vert:
                rr: int
                cc: int
                rr, cc, = coord
                if rr == r:
                    between_rows[cc * 4] = "|"
            for coord in diag_slash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = "/"
            for coord in diag_backslash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = "\\"
        
        print("LL " + "".join(between_rows) + "RR")

    found_count = len(connections)
    total = len(strands.answers())
    footer_text = f"Found {found_count}/{total}  Hint 0"
    print("LL " + footer_text + (" " * ((4 * columns) - 19)) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))


def play_game():
    game: StrandsGameBase = StrandsGameStub("filename", hint_threshold = 3)

    while not game.game_over():
        update_display(game, game.found_strands())
        key = input("> ")
        if key == "q":
            break
        if key == "":
            game.submit_strand(None)
    
    update_display(game, game.found_strands())

if __name__ == "__main__":
    play_game()
