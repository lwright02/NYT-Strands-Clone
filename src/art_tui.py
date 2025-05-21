import sys
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

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == "wrappers":
        fw, width, height = map(int, args[1:])
        TUIStub(ArtTUIWrappers(fw, width), width, height)
    elif args[0] == "cat1":
        fw, width, height = map(int, args[1:])
        ArtTUICat1(fw, width).print_frame(height)
    elif args[0] == "cat2":
        fw, width, height = map(int, args[1:])
        ArtTUICat2(fw, width).print_frame(height)
    else:
        print(f"Pattern '{args[0]}' is not supported in TUI.")
