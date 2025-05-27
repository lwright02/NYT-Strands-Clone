"""
TUI for Strands
"""

# Remark I: The getch function is giving us a mypy error. I went to my TA 
# to ask for help in discussion section, and he tried to help, but we could not
# resolve the issue. He said it was fine if I submited as is with the mypy 
# issues. 

# Remark II: We have to define the type of the frame like it is done throughout
# the code (i.e. not using ArtTUIBase) because we added a few attributes, and
# we could not addd any attributes to ArtTUIBase (it says to not modify that 
# file). Thus, we just said it was one of the sub-types, each has our attribute
# with a type. 

import sys
import termios
import tty
import click
import random
import os
import re

ANSI_ESCAPE_PATTERN = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

from strands import Pos, Strand, Board, StrandsGame
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase
from art_tui import ArtTUIBase, ArtTUISpecial, ArtTUIWrappers, ArtTUICat1, ArtTUICat2
from ui import ArtTUIStub

key_Enter: int = 13
key_Esc: int = 27
key_Up: str = "\033[A"
key_Dn: str = "\033[B"
key_Rt: str = "\033[C"
key_Lt: str = "\033[D"

fdInput: int = sys.stdin.fileno()
termAttr = termios.tcgetattr(0)

def getch() -> str | int:
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


def update_display(strands: StrandsGame, connections: list[StrandBase], 
                   current_pos: Pos, selected: list[Pos], 
                   frame: ArtTUISpecial | ArtTUIWrappers | ArtTUICat1 | ArtTUICat2 | ArtTUIStub) -> None:
    """
    Given all the words that have been found, this function will print what
    the board looks like at a given time. The found words are highlighted, and
    there is a tracker of how many words you've found and how many hints you've
    used at the bottom of the game. There will also be highlighted text and 
    connections to indicate the characters you currently have selected.
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
        p_1: PosBase = selected[i]
        p_2: PosBase = selected[i+1]
        r_1: int
        c_1: int
        r_1, c_1 = p_1.r, p_1.c
        r_2: int
        c_2: int
        r_2, c_2 = p_2.r, p_2.c
        d_r: int
        d_c: int
        d_r = r_2 - r_1
        d_c = c_2 - c_1
        if d_r == 0:
            selected_horiz.add((r_1, min(c_1, c_2)))
        elif d_c == 0:
            selected_vert.add((min(r_1, r_2), c_1))
        else:
            if (d_r, d_c) == (1, 1) or (d_r, d_c) == (-1, -1):
                selected_diag_backslash.add((min(r_1, r_2), min(c_1, c_2)))
            else:
                selected_diag_slash.add((min(r_1, r_2), min(c_1, c_2)))

    hint: None | tuple[int, bool] = strands.active_hint()
    hint_pos: set[tuple[int, int]] = set()
    hint_end: set[tuple[int, int]] = set()
    if hint is not None:
        i2: int
        show_end: bool
        i2, show_end = hint
        _, hstrand = strands.answers()[i2]
        hpos = hstrand.positions()
        if show_end:
            for p in hpos:
                hint_pos.add((p.r, p.c))
            hint_end.add((hpos[0].r, hpos[0].c))
            hint_end.add((hpos[-1].r, hpos[-1].c))
        else:
            for p in hpos:
                hint_pos.add((p.r, p.c))

    found_pos: list[tuple[int, int]] = []
    for strand in connections:
        for p in strand.positions():
            coord: tuple[int, int] = (p.r, p.c)
            if coord not in found_pos:
                found_pos.append(coord)

    rows_and_connectors: list[tuple[str, str]] = []

    for r in range(rows):
        line_chars: list[str] = []
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
                    display = display + bold + green + " - " + reset
                elif (r, c) in horiz:
                    display = display + bold + blue + " - " + reset
                else:
                    display = display + "   "
            else:
                display = display + " "
            line_chars.append(display)
        row_line: str = "".join(line_chars)

        between_rows: list[str] = []
        for _ in range(4 * columns - 2):
            between_rows.append(" ")
        if r < rows - 1:
            for rr, cc in vert:
                if rr == r:
                    between_rows[cc * 4] = bold + blue + "|" + reset
            for rr, cc in diag_slash:
                if rr == r and between_rows[cc * 4 + 2] == " ":
                    between_rows[cc * 4 + 2] = bold + blue + "/" + reset
            for rr, cc in diag_backslash:
                if rr == r and between_rows[cc * 4 + 2] == " ":
                    between_rows[cc * 4 + 2] = bold + blue + "\\" + reset
                elif rr == r and between_rows[cc * 4 + 2] == bold + blue + "/" + reset:
                    between_rows[cc * 4 + 2] = bold + blue + "X" + reset

            for rr, cc in selected_vert:
                if rr == r:
                    between_rows[cc * 4] = bold + green + "|" + reset
            for rr, cc in selected_diag_slash:
                if (rr == r 
                    and between_rows[cc * 4 + 2] == bold + blue + "\\" + reset):
                    between_rows[cc * 4 + 2] = bold + green + "X" + reset
                elif rr == r:
                    between_rows[cc * 4 + 2] = bold + green + "/" + reset
            for rr, cc in selected_diag_backslash:
                if (rr == r 
                    and between_rows[cc * 4 + 2] != bold + blue + "\\" + reset 
                    and between_rows[cc * 4 + 2] !=  " "):
                    between_rows[cc * 4 + 2] = bold + green + "X" + reset
                elif rr == r:
                    between_rows[cc * 4 + 2] = bold + green + "\\" + reset
            between_line = "".join(between_rows)
            rows_and_connectors.append((row_line, between_line))
        else:
            rows_and_connectors.append((row_line, ""))  

    found_count = len(connections)
    total = len(strands.answers())
    hint_meter = strands.hint_meter()
    hint_threshold = strands.hint_threshold()
    footer_text = f"Found {found_count}/{total}  Hint {hint_meter}/{hint_threshold}"

    frame.interior_width = len(ANSI_ESCAPE_PATTERN.sub('', rows_and_connectors[0][0]))
    frame.print_top_edge()
    for row_line, between_line in rows_and_connectors:
        frame.print_left_bar()
        print(row_line, end="")
        frame.print_right_bar()
        if row_line != rows_and_connectors[-1][0]:
            frame.print_left_bar()
            print(between_line, end="")
            frame.print_right_bar()
    
    frame.print_left_bar()
    print(footer_text + 
          (" " * ((4 * columns) - (len(footer_text) + 2))), end = "")
    frame.print_right_bar()

    score_text = f"Score: {strands.get_score()}"
    spaces = " " * ((4 * columns) - (len(score_text) + 2))
    frame.print_left_bar()
    print(score_text + spaces, end = "")
    frame.print_right_bar()

    frame.print_bottom_edge()

def play_game(game_file: str, frame: ArtTUISpecial | ArtTUIWrappers | ArtTUICat1 | ArtTUICat2 | ArtTUIStub, 
              show: bool = False, hint_threshold: int = 3) -> None:
    """
    Allows for the game to be run in the terminal.
    """
    game: StrandsGame = StrandsGame(game_file, hint_threshold)
    current_pos = Pos(0, 0)
    selected = [current_pos]
    board: Board = game.board()
    rows: int = board.num_rows()
    columns: int = board.num_cols()
    
    if show: 
        connections = []
        for _, strand in game.answers():
            connections.append(strand)
        update_display(game, connections, Pos(0, 0), [], frame)

    else:
        while not game.game_over():

            update_display(game, game.found_strands(), current_pos, selected, frame)
            key = getch()
            key_dict = {"7": (-1, -1), "8": (-1, 0), "9": (-1, 1),
                        "4": (0, -1), "6": (0, 1),
                        "1": (1, -1), "2": (1, 0), "3": (1, 1)}
            if key == "q":
                break

            elif isinstance(key, str) and key in key_dict:
                dr, dc = key_dict[key]
                new_r = current_pos.r + dr
                new_c = current_pos.c + dc
                if 0 <= new_r < rows and 0 <= new_c < columns:
                    new_pos = Pos(new_r, new_c)
                    if new_pos in selected:
                        cut = selected.index(new_pos) + 1
                        selected = selected[:cut]
                    else:
                        selected.append(new_pos)
                    current_pos = new_pos

            elif key == 27:
                selected = [current_pos]

            elif key == "h":
                if game._hint_meter >= game.hint_threshold():
                    game.use_hint()
                else:
                    print("Can't use a hint")
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
                game.submit_strand(Strand(selected[0], steps_enum))
                selected = [current_pos]
            update_display(game, game.found_strands(), current_pos, selected, frame)


@click.command()
@click.option("--show",    is_flag=True, help="Show the answers instead of playing the game.")
@click.option("--special", is_flag=True, help="Play the custom game.")
@click.option(
    "-g",
    "--game",
    "game",
    type=str,
    help="Game to load (ex: cs-142). Loads a random game if not provided.",
)
@click.option(
    "-h",
    "--hint",
    "hint",
    type=int,
    default=3,
    show_default=True,
    help="Hint threshold (default: 3).",
)
@click.option(
    "-a",
    "--art",
    "art",
    type=click.Choice(["wrappers", "cat1", "cat2"]),
    help="Art frame to use (ex: stub, cat1). Supports wrappers, cat1, and cat2. Uses stubs if not provided.",
)
def main(show: bool, special: bool, game: str | None, hint: int, art: str | None) -> None:
    if special:
        game_file = os.path.join("assets", "Customized.txt")
    else:
        board = "boards"
        try:
            files = os.listdir(board)
        except OSError:
            click.echo(f"Cannot list '{board}'", err=True)
            sys.exit(1)
        games = [f[:-4] for f in files if f.lower().endswith(".txt")]
        if not games:
            click.echo(f"No .txt files in '{board}'", err=True)
            sys.exit(1)
        if not game or game not in games:
            if game:
                click.echo(f"Unknown game '{game}', picking random.", err=True)
            game = random.choice(games)
        game_file = os.path.join(board, f"{game}.txt")

    strandgame: StrandsGame = StrandsGame(game_file, hint)
    interior = 4 * (strandgame.board().num_cols() - 1) + 1

    frame: ArtTUISpecial | ArtTUIWrappers | ArtTUICat1 | ArtTUICat2 | ArtTUIStub
    if special:
        frame = ArtTUISpecial(1, interior)
    elif art == "wrappers":
        frame = ArtTUIWrappers(1, interior)
    elif art == "cat1":
        frame = ArtTUICat1(3, interior)
    elif art == "cat2":
        frame = ArtTUICat2(3, interior)
    else:
        frame = ArtTUIStub(1, interior)

    play_game(game_file, frame, show=show, hint_threshold=hint)

if __name__ == "__main__":
    main()