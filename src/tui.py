"""
TUI for Strands
"""

import sys
import termios
import tty
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake
from stubs import PosStub, StrandStub, BoardStub, StrandsGameStub
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase


fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

def getch() -> str:
    """
    Slightly modified version of getch function from stackexchange link posted
    on canvas.
    """
    try:
        tty.setraw(fdInput)
        ch = sys.stdin.buffer.read(1)
        return ch.decode(sys.stdin.encoding or "utf-8", errors="ignore")
    finally:
        termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)


def update_display(strands: StrandsGameBase, connections: list[StrandBase], 
                   current_pos: Pos, selected: list[Pos]) -> None:
    """
    Given all the words that have been found, this function will print what
    the board looks like at a given time. The found words are highlighted, and
    there is a tracker of how many words you've found and how many hints you've
    used at the bottom of the game. There will also be highlighted text and 
    connections to indicate the characters you currently have selected
    """
    board: BoardBase = strands.board()
    rows: int = board.num_rows()
    columns: int = board.num_cols()
    bold: str = "\033[1m"
    reset: str = "\033[0m"
    blue: str = "\033[34m"
    green: str = "\033[32m"
    red: str = "\033[31m"

    horiz: set[tuple[int, int]] = set()
    vert: set[tuple[int, int]] = set()
    diag_slash: set[tuple[int, int]] = set()
    diag_backslash: set[tuple[int, int]] = set()
    for strand in connections:
        positions: list[PosBase] = strand.positions()
        for i, _ in enumerate(positions[:-1]):
            p1: PosBase = positions[i]
            p2: PosBase = positions[i+1]
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

    selected_horiz: set[tuple[int, int]] = set()
    selected_vert: set[tuple[int, int]] = set()
    selected_diag_slash: set[tuple[int, int]] = set()
    selected_diag_backslash: set[tuple[int, int]] = set()
    for i, _ in selected[:-1]:
        p1: PosBase = selected[i]
        p2: PosBase = selected[i+1]
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
            selected_horiz.add((r1, min(c1, c2)))
        elif dc == 0:
            selected_vert.add((min(r1, r2), c1))
        else:
            if (dr, dc) == (1, 1) or (dr, dc) == (-1, -1):
                selected_diag_backslash.add((min(r1, r2), min(c1, c2)))
            else:
                selected_diag_slash.add((min(r1, r2), min(c1, c2)))


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
            if (r, c) == current_pos:
                display = bold + red + letter + reset
            elif (r, c) in found_pos:
                display = bold + blue + letter + reset
            elif(r, c) in selected:
                display = bold + green + letter + reset
            else:
                display = letter
            if c < columns - 1:
                if (r, c) in horiz:
                    print(display + bold + blue + " - " + reset, end = "")
                elif (r, c) in selected_horiz:
                    print(display + bold + green + " - " + reset, end = "")
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
                    between_rows[cc * 4] = bold + blue + "|" + reset
            for coord in diag_slash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = bold + blue + "/" + reset
            for coord in diag_backslash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = bold + blue + "\\" + reset
            for coord in selected_vert:
                rr: int
                cc: int
                rr, cc, = coord
                if rr == r:
                    between_rows[cc * 4] = bold + green + "|" + reset
            for coord in selected_diag_slash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = bold + green + "/" + reset
            for coord in selected_diag_backslash:
                rr, cc = coord
                if rr == r:
                    between_rows[cc * 4 + 2] = bold + green + "\\" + reset
        print("LL " + "".join(between_rows) + "RR")

    found_count = len(connections)
    total = len(strands.answers())
    footer_text = f"Found {found_count}/{total}  Hint 0"
    print("LL " + footer_text + (" " * ((4 * columns) - 19)) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))


def play_game() -> None:
    """
    Allows for the game to be run in the terminal.
    """
    game: StrandsGameBase = StrandsGameStub("filename", hint_threshold = 3)

    while not game.game_over():
        update_display(game, game.found_strands())
        key = getch()
        if key == "q":
            break
        if key == "\r":
            _, next_strand = game.answers()[len(game.found_strands())]
            game.submit_strand(next_strand)
    
    update_display(game, game.found_strands())

if __name__ == "__main__":

    if sys.argv[2] == "play":
        play_game()
    elif sys.argv[2] == "show":
        strand = StrandBase(sys.argv[3])
        update_display(strand, conn)
