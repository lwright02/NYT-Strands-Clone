"""
Abstract base classes and stubs for Strands game UIs.

There are two ABCs, called ArtTUIBase and ArtGUIBase, which
describe the interfaces that the TUI and GUI expect the Art
components to satisfy.

There are two stub implementations, called ArtTUIStub and
ArtGUIStub, of these base classes. These stub
implementations are intended to be used by the TUI and GUI
designers in the early stages of the project, before the
Artist has done their work.

There are also two stub classes, called TUIStub and GUIStub
(which have no prescribed ABCs). These are intended to be
used by the Artist in the early stages of the project,
before the TUI and GUI designers have done their work.

Do not modify this file.
"""
from abc import ABC, abstractmethod
import pygame
import sys


class ArtTUIBase(ABC):
    """
    Interface for Art TUI component.
    """

    @abstractmethod
    def __init__(self, frame_width: int, interior_width: int):
        """
        Constructor

        The frame_width is nominally the required
        height (in characters) for the top and bottom
        edges and the required width (in characters)
        for the left and right edges. However, the
        actual width for left and right edges can
        be a multiple of frame_width, if desired,
        to help account for the fact that characters
        are taller than they are wide.

        The interior_width is the expected width (in
        characters) for each line in the interior
        printed by the TUI.
        """
        raise NotImplementedError

    @abstractmethod
    def print_top_edge(self) -> None:
        """
        Print the top edge of the overall text display.
        Depending on the frame_width, multiple lines
        may be printed.
        """
        raise NotImplementedError

    @abstractmethod
    def print_bottom_edge(self) -> None:
        """
        Print the bottom edge of the overall text display.
        Depending on the frame_width, multiple lines
        may be printed.
        """
        raise NotImplementedError

    @abstractmethod
    def print_left_bar(self) -> None:
        """
        Print a single line of the left bar to precede a
        line of the TUI display. The left bar should not
        conclude with a newline.
        """
        raise NotImplementedError

    @abstractmethod
    def print_right_bar(self) -> None:
        """
        Print a single line of the right bar to follow a
        line of the TUI display. The right bar should
        conclude with a newline.
        """
        raise NotImplementedError


class ArtGUIBase(ABC):
    """
    Interface for Art GUI component.
    """

    frame_width: int

    @abstractmethod
    def __init__(self, frame_width: int):
        """
        Constructor

        The frame_width is the required height (in pixels)
        for the top and bottom edges and the required width
        (in pixels) for the left and right edges.
        """
        raise NotImplementedError

    @abstractmethod
    def draw_background(self, surface: pygame.Surface) -> None:
        """
        Draw to the entire window, expecting that the GUI
        will draw over the interior thus leaving only the
        frame visible. The window dimensions are available
        via surface.get_width() and surface.get_height().
        """
        raise NotImplementedError


class ArtTUIStub(ArtTUIBase):
    """
    Stub ArtTUI implementation.

    With a frame_width of 2, for example, the generated
    frame surrounds an interior as follows:

        TOP---------
        TOP---------
        LL        RR
        LL        RR
        LL        RR
        LL        RR
        LL        RR
        BOTTOM------
        BOTTOM------
    """

    frame_width: int
    interior_width: int

    def __init__(self, frame_width: int, interior_width: int):
        """See ArtTUIBase and ArtTUIStub"""
        self.frame_width = frame_width
        self.interior_width = interior_width

    def print_top_edge(self) -> None:
        """See ArtTUIBase and ArtTUIStub"""
        n = self.interior_width + 2 * (self.frame_width + 1)
        for _ in range(self.frame_width):
            print("TOP".ljust(n, "-"))

    def print_bottom_edge(self) -> None:
        """See ArtTUIBase and ArtTUIStub"""
        n = self.interior_width + 2 * (self.frame_width + 1)
        for _ in range(self.frame_width):
            print("BOTTOM".ljust(n, "-"))

    def print_left_bar(self) -> None:
        """See ArtTUIBase and ArtTUIStub"""
        left = self.frame_width * "L"
        print(f"{left} ", end="")

    def print_right_bar(self) -> None:
        """See ArtTUIBase and ArtTUIStub"""
        right = self.frame_width * "R"
        print(f" {right}")


class ArtGUIStub(ArtGUIBase):
    """
    Stub ArtGUI implementation.

    Draws a gray background to the entire window.
    """

    frame_width: int

    def __init__(self, frame_width: int):
        """See ArtGUIBase and ArtGUIStub"""
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        """See ArtGUIBase and ArtGUIStub"""
        width = surface.get_width()
        height = surface.get_height()
        pygame.draw.rect(
            surface, color=(150, 150, 150), rect=(0, 0, width, height)
        )


class TUIStub:
    """
    Stub TUI implementation, which prints a blank interior.
    """

    _art: ArtTUIBase
    _width: int
    _height: int

    def __init__(self, art: ArtTUIBase, width: int, height: int):
        """
        Constructor
        """
        self._art = art
        self._width = width
        self._height = height
        self.print_display()

    def print_display(self) -> None:
        """
        Print the overall text display, using the art
        component to draw top and bottom edges plus left
        and right bars around each (blank) interior line.
        """
        self._art.print_top_edge()
        for _i in range(self._height):
            self._art.print_left_bar()
            print(self._width * " ", end="")
            self._art.print_right_bar()
        self._art.print_bottom_edge()


class GUIStub:
    """
    Stub GUI implementation, which draws a blank interior.
    """

    _art: ArtGUIBase
    _surface: pygame.Surface
    _clock: pygame.time.Clock

    def __init__(self, art: ArtGUIBase, width: int, height: int):
        """
        Constructor
        """
        self._art = art

        pygame.init()
        self._surface = pygame.display.set_mode((width, height))
        self._clock = pygame.time.Clock()

    def run_event_loop(self) -> None:
        """
        Draw the overall graphical display, using the art
        component to draw the background. This stub does
        not draw any interior.
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self._art.draw_background(self._surface)
            pygame.display.flip()
            self._clock.tick(24)
