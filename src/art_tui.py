import sys
import click
from ui import ArtTUIBase, TUIStub

CHARS = ['#', '@', '%', '=', '+', '.']

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

    def print_top_edge(self) -> None:
        pass
    def print_bottom_edge(self) -> None:
        pass
    def print_left_bar(self) -> None:
        pass
    def print_right_bar(self) -> None:
        pass

    def print_frame(self, height: int) -> None:
        for row in range(height):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                if col % 2 == 0:
                    line += '|'
                else:
                    line += ' '
            print(line)

class ArtTUICat2(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width

    def print_top_edge(self) -> None:
        pass
    def print_bottom_edge(self) -> None:
        pass
    def print_left_bar(self) -> None:
        pass
    def print_right_bar(self) -> None:
        pass

    def print_frame(self, height: int) -> None:
        for row in range(height):
            line = ""
            for col in range(self.interior_width + 2 * self.frame_width):
                if (row + col) % 4 == 0:
                    line += "/"
                elif (row - col) % 4 == 0:
                    line += "\\"
                else:
                    line += " "
            print(line)

class ArtTUISpecial(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width
    
    def print_top_edge(self) -> None:
        pattern: str = "S T E A K"
        pad: str = max(0, self.interior_width - len(pattern))
        print("# " + pattern + " " * pad + " #")

    def print_bottom_edge(self) -> None:
        pattern = "S H I R T"
        pad = max(0, self.interior_width - len(pattern))
        print("# " + pattern + " " * pad + " #")
    
    def print_left_bar(self) -> None:
        print("#", end="")

    def print_right_bar(self) -> None:
        print("#")

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

    if art in {"cat4", "steak", "special"}:
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