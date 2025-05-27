import sys
import click
from ui import ArtTUIBase, TUIStub
import random

CHARS = ['#', '@', '%', '=', '+', '.']

reset: str = "\033[0m"
blue: str = "\033[34m"
green: str = "\033[32m"
red: str = "\033[31m"
pink: str = "\033[35m"
colors = [blue, green, red, pink]

class ArtTUIWrappers(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width

    def print_top_edge(self) -> None:
        full_width = self.interior_width + 2 * (self.frame_width + 1) - 2
        for i in range(self.frame_width):
            char = CHARS[i % len(CHARS)]
            print(char * full_width)

    def print_bottom_edge(self) -> None:
        full_width = self.interior_width + 2 * (self.frame_width + 1) - 2
        for i in reversed(range(self.frame_width)):
            char = CHARS[i % len(CHARS)]
            print(char * full_width)

    def print_left_bar(self) -> None:
        for i in range(self.frame_width):
            char = CHARS[i % len(CHARS)]
            print(char, end="")

    def print_right_bar(self) -> None:
        for i in reversed(range(self.frame_width)):
            char = CHARS[i % len(CHARS)]
            print(char, end="")
        print()

    def print_frame(self, height: int) -> None:
        self.print_top_edge()
        for _ in range(height):
            self.print_left_bar()
            print(" " * self.interior_width, end="")
            self.print_right_bar()
        self.print_bottom_edge()

class ArtTUICat1(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width
        self.interior_height = 0

    def _get_pattern_char(self, col: int) -> str:
        return '|' if col % 2 == 0 else ' '

    def print_top_edge(self) -> None:
        for row in range(self.frame_width):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                line += self._get_pattern_char(col)
            print(line)

    def print_bottom_edge(self) -> None:
        for row in range(self.frame_width):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                line += self._get_pattern_char(col)
            print(line)

    def print_left_bar(self) -> None:
        for col in range(self.frame_width):
            print(self._get_pattern_char(col), end="")

    def print_right_bar(self) -> None:
        offset = self.frame_width + self.interior_width
        for col in range(self.frame_width):
            print(self._get_pattern_char(offset + col), end="")
        print()

    def print_frame(self, height: int) -> None:
        self.interior_height = height
        self.print_top_edge()
        for row in range(height):
            line = ""
            for col in range(self.frame_width + self.interior_width + self.frame_width):
                line += self._get_pattern_char(col)
            print(line)
        self.print_bottom_edge()

class ArtTUICat2(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width
        self.interior_height = 0

    def _get_pattern_char(self, col: int) -> str:
        return '>' if col % 2 == 0 else '<'

    def print_top_edge(self) -> None:
        for row in range(self.frame_width):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                line += self._get_pattern_char(col)
            print(line)

    def print_bottom_edge(self) -> None:
        for row in range(self.frame_width):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                line += self._get_pattern_char(col)
            print(line)

    def print_left_bar(self) -> None:
        for col in range(self.frame_width):
            print(self._get_pattern_char(col), end="")

    def print_right_bar(self) -> None:
        offset = self.frame_width + self.interior_width
        for col in range(self.frame_width):
            print(self._get_pattern_char(offset + col), end="")
        print()

    def print_frame(self, height: int) -> None:
        self.interior_height = height
        self.print_top_edge()
        for row in range(height):
            line = ""
            for col in range(self.frame_width + self.interior_width + self.frame_width):
                line += self._get_pattern_char(col)
            print(line)
        self.print_bottom_edge()

class ArtTUISpecial(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width
    
    def print_top_edge(self) -> None:
        pattern: str = "SPECIAL STUFF"
        pad: int = max(0, self.interior_width - len(pattern) - 1)
        color = random.choice(colors)
        print(color + "# " + pattern + " " * pad + " #" + reset)

    def print_bottom_edge(self) -> None:
        pattern = "SPECIAL STUFF"
        pad = max(0, self.interior_width - len(pattern) - 1)
        color = random.choice(colors)
        print(color + "# " + pattern + " " * pad + " #" + reset)
    
    def print_left_bar(self) -> None:
        color = random.choice(colors)
        print(color + "#" + reset, end="")

    def print_right_bar(self) -> None:
        color = random.choice(colors)
        print(color + "#" + reset)

    def print_frame(self, height: int) -> None:
        for row in range(height):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                if (row + col) % 4 == 0:
                    line += "?"
                elif (row - col) % 4 == 0:
                    line += "!"
                else:
                    line += " "
            print(line)

@click.command()
@click.option('-a', '--art', required=True, help="Art frame: wrappers, cat1, cat2, special.")
@click.option('-f', '--frame', type=int, help="Frame width (characters).")
@click.option('-w', '--width', type=int, help="Interior width (columns).")
@click.option('-h', '--height', type=int, help="Interior height (rows).")
def main(art, frame, width, height):
    supported = {
        "wrappers": ArtTUIWrappers,
        "cat0": ArtTUIWrappers,
        "cat1": ArtTUICat1,
        "cat2": ArtTUICat2,
        "special": ArtTUISpecial
    }

    if art not in supported:
        click.echo(f"Pattern '{art}' is not supported in TUI.")
        return

    cls = supported[art]

    if art in {"cat4", "special"}:
        tui = cls(0, 20)
        tui.print_frame(10)
    else:
        if frame is None or width is None or height is None:
            click.echo("Missing options: --frame, --width, and --height are required unless using cat4/special.")
            return
        tui = cls(frame, width)
        tui.print_frame(height)

if __name__ == "__main__":
    main()