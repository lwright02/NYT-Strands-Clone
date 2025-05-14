"""
TUI for Strands
"""

import sys
import termios
import tty
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake, STEPS
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase

key_Enter = 13
key_Esc = 27
key_Up = "\033[A"
key_Dn = "\033[B"
key_Rt = "\033[C"
key_Lt = "\033[D"

fdInput = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

def getch():
    """
    getch function from Canvas page
    """
    tty.setraw(fdInput)
    ch = sys.stdin.buffer.raw.read(4).decode(sys.stdin.encoding)
    if len(ch) == 1:
        if ord(ch) < 32 or ord(ch) > 126:
            ch = ord(ch)
    elif ord(ch[0]) == 27:
        ch = "\033" + ch[1:]
    termios.tcsetattr(fdInput, termios.TCSADRAIN, termAttr)
    return ch


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
    pink: str = "\033[35m"

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
    for i, _ in enumerate(selected[:-1]):
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

    hint = strands.active_hint()
    hint_pos: set[tuple[int, int]] = set()
    hint_end: set[tuple[int, int]] = set()
    if hint is not None:
        idx, show_end = hint
        _, hstrand = strands.answers()[idx]
        hpos = hstrand.positions()
        if show_end:
            for p in hpos:
                hint_pos.add((p.r, p.c))
            hint_end.add((hpos[0].r, hpos[0].c))
            hint_end.add((hpos[-1].r, hpos[-1].c))
        else:
            for p in hpos[1:-1]:
                hint_pos.add((p.r, p.c))

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
            if (r, c) == (current_pos.r, current_pos.c):
                display = bold + red + letter + reset
            elif Pos(r, c) in selected:
                display = bold + green + letter + reset
            elif (r, c) in hint_pos:
                if (r, c) in hint_end:
                    display = bold + pink + letter + reset
                else:
                    display = pink + letter + reset
            elif (r, c) in found_pos:
                display = bold + blue + letter + reset
            else:
                display = letter
            if c < columns - 1:
                if (r, c) in selected_horiz:
                    print(display + bold + green + " - " + reset, end = "")
                elif (r, c) in horiz:
                    print(display + bold + blue + " - " + reset, end = "")
                else:
                    print(display + "   ", end = "")
            else:
                print(display + " ", end = "")
        print("RR")
        between_rows: list[str] = []
        for _ in range(4 * columns - 2):
            between_rows.append(" ")
        if r < rows - 1:
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
        print("LL " + "".join(between_rows) + "RR")

    found_count = len(connections)
    total = len(strands.answers())
    hint_meter = strands.hint_meter()
    hint_threshold = strands.hint_threshold()
    footer_text = f"Found {found_count}/{total}  Hint {hint_meter}/{hint_threshold}"
    print("LL " + footer_text + 
          (" " * ((4 * columns) - (len(footer_text) + 2))) + "RR")
    print("LL" + (" " * ((4 * columns) - 1)) + "RR")
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))
    print("BOTTOM" + ("-" * ((4 * columns) - 3)))


def play_game(game_file) -> None:
    """
    Allows for the game to be run in the terminal.
    """
    game: StrandsGameBase = StrandsGameFake(game_file, hint_threshold = 3)
    current_pos = Pos(0, 0)
    selected = [current_pos]
    board: BoardBase = game.board()
    rows: int = board.num_rows()
    columns: int = board.num_cols()

    while not game.game_over():

        update_display(game, game.found_strands(), current_pos, selected)
        key = getch()
        key_dict = {"1": (-1, -1), "2": (-1, 0), "3": (-1, 1),
                    "4": (0, -1), "6": (0, 1),
                    "7": (1, -1), "8": (1, 0), "9": (1, 1)}
        if key == "q":
            break

        elif key in key_dict:
            dr, dc = key_dict[key]
            new_r = current_pos.r + dr
            new_c = current_pos.c + dc
            if 0 <= new_r < rows and 0 <= new_c < columns:
                current_pos = Pos(new_r, new_c)
                selected.append(current_pos)

        elif key == 27:
            selected = [current_pos]

        elif key == "h":
            if game._hint_meter < game.hint_threshold():
                game._hint_meter += 1
                game.use_hint()
            continue

        elif key == 13 or key == "5":
            steps_enum = []
            for i, _ in enumerate(selected[:-1]):
                p1 = selected[i]
                p2 = selected[i+1]
                dr = p2.r - p1.r
                dc = p2.c - p1.c
                if (dr, dc) == (-1, 0):
                    steps_enum.append(Step.N)
                elif (dr, dc) == (1, 0):
                    steps_enum.append(Step.S)
                elif (dr, dc) == (0, 1):
                    steps_enum.append(Step.E)
                elif (dr, dc) == (0, -1):
                    steps_enum.append(Step.W)
                elif (dr, dc) == (-1, 1):
                    steps_enum.append(Step.NE)
                elif (dr, dc) == (-1, -1):
                    steps_enum.append(Step.NW)
                elif (dr, dc) == (1, 1):
                    steps_enum.append(Step.SE)
                elif (dr, dc) == (1, -1):
                    steps_enum.append(Step.SW)
            game.submit_strand(StrandFake(selected[0], steps_enum))
            selected = [current_pos]
        update_display(game, game.found_strands(), current_pos, selected)


if __name__ == "__main__":

    if sys.argv[1] == "play":
        game_file = sys.argv[2]
        play_game(game_file)
    
    elif sys.argv[1] == "show":
        game_file = sys.argv[2]
        game = StrandsGameFake(game_file, hint_threshold=3)
        connections = []
        for _, strand in game.answers():
            connections.append(strand)
        update_display(game, connections, Pos(0, 0), [])