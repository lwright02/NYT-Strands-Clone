"""
Game logic for Milestone 2:
Pos, Strand, Board, StrandsGame
"""
from typing import TypeAlias
from base import PosBase, StrandBase, BoardBase, StrandsGameBase, Step

Row: TypeAlias = int
Col: TypeAlias = int

class Pos(PosBase):
    """
    See ABC docstring.
    """

    r: Row
    c: Col

    def __init__(self, r: Row, c: Col) -> None:
        """
        See ABC docstring.
        """
        self.r = r
        self.c = c

    def take_step(self, step: Step) -> "Pos":
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def step_to(self, other: "Pos") -> Step:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def is_adjacent_to(self, other: "Pos") -> bool:
        """
        See ABC docstring.
        """
        raise NotImplementedError

######################################################################


class Strand(StrandBase):
    """
    Strands, represented as a start position
    followed by a sequence of steps.
    """

    start: PosBase
    steps: list[Step]

    def __init__(self, start: PosBase, steps: list[Step]):
        """
        See ABC docstring.
        """
        self.start = start
        self.steps = steps

    def positions(self) -> list[Pos]:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def is_cyclic(self) -> bool:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def is_folded(self) -> bool:
        """
        See ABC docstring.
        """
        raise NotImplementedError

######################################################################


class Board(BoardBase):
    """
    Boards for the Strands game, consisting of a
    rectangular grid of letters.
    """

    
    def __init__(self, letters: list[list[str]]):
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def num_rows(self) -> int:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def num_cols(self) -> int:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def get_letter(self, pos: Pos) -> str:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def evaluate_strand(self, strand: Strand) -> str:
        """
        See ABC docstring.
        """
        raise NotImplementedError


######################################################################


class StrandsGame(StrandsGameBase):
    """
    Abstract base class for Strands game logic.
    """
    def __init__(self, game_file: str | list[str], hint_threshold: int = 3):
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def theme(self) -> str:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def board(self) -> BoardBase:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def answers(self) -> list[tuple[str, Strand]]:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    
    def found_strands(self) -> list[Strand]:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def game_over(self) -> bool:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def hint_threshold(self) -> int:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def hint_meter(self) -> int:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def active_hint(self) -> None | tuple[int, bool]:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def submit_strand(self, strand: Strand) -> tuple[str, bool] | str:
        """
        See ABC docstring.
        """
        raise NotImplementedError

    def use_hint(self) -> tuple[int, bool] | str:
        """
        See ABC docstring.
        """
        raise NotImplementedError