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

if __name__ == "__main__":
    fw, width, height = map(int, sys.argv[1:])
    TUIStub(ArtTUIWrappers(fw, width), width, height)
