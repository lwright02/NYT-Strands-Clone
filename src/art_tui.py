import sys
from ui import ArtTUIBase, TUIStub  # adjust import as needed

class ANSI:
    COLORS = [
        "\033[38;5;204m",
        "\033[38;5;113m",
        "\033[38;5;117m",
        "\033[38;5;221m",
        "\033[38;5;141m",
        "\033[38;5;186m"
    ]
    RESET = "\033[0m"

class ArtTUIWrappers(ArtTUIBase):
    def __init__(self, frame_width: int, interior_width: int):
        self.frame_width = frame_width
        self.interior_width = interior_width

    def print_top_edge(self) -> None:
        for i in reversed(range(self.frame_width)):
            color = ANSI.COLORS[(self.frame_width - 1 - i) % len(ANSI.COLORS)]
            print(" " * (self.frame_width - i) + color + "█" * (self.interior_width + 2 * i + 2) + ANSI.RESET)

    def print_bottom_edge(self) -> None:
        for i in range(self.frame_width):
            color = ANSI.COLORS[(self.frame_width - 1 - i) % len(ANSI.COLORS)]
            print(" " * (self.frame_width - i) + color + "█" * (self.interior_width + 2 * i + 2) + ANSI.RESET)

    def print_left_bar(self) -> None:
        line = [" "] * (self.frame_width + 1)
        for i in range(self.frame_width):
            color = ANSI.COLORS[i % len(ANSI.COLORS)]
            line[i] = color + "█" + ANSI.RESET
        print("".join(line), end="")

    def print_right_bar(self) -> None:
        line = [" "] * (self.frame_width + 1)
        for i in range(self.frame_width):
            color = ANSI.COLORS[i % len(ANSI.COLORS)]
            line[self.frame_width - i] = color + "█" + ANSI.RESET
        print("".join(line))

if __name__ == "__main__":
    fw, width, height = map(int, sys.argv[1:])
    TUIStub(ArtTUIWrappers(fw, width), width, height)
