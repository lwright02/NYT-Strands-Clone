"""
Game logic stubs: PosStub, StrandStub, BoardStub, StrandsGameStub

This stub implementation behaves as follows:

- The "CS 142" game, described in boards/cs-142.txt, is
  hard-coded into the implementation. The actual text file
  is not used at all.

- The 3x5 board is hard-coded with the rows:
  CSMCT, OFORY, and NEOWT

- There are four hard-coded answer strands, corresponding
  to CMSC, ONE, FORTY, and TWO.

- When a strand is submitted to the game for consideration
  as a new theme or dictionary word, the strand argument is
  completely ignored, and the game automatically "finds" the
  next of the four hard-coded answer strands.

- The hint feature is not attempted at all.

- Several methods return simple, unhelpful results (as
  opposed to raising NotImplementedErrors).
"""

from base import BoardBase, PosBase, Step, StrandBase, StrandsGameBase


class PosStub(PosBase):
    """
    Stub position class.
    Constructor inherited, no methods implemented.
    """

    def take_step(self, step: Step) -> PosBase:
        raise NotImplementedError

    def step_to(self, other: PosBase) -> Step:
        raise NotImplementedError

    def is_adjacent_to(self, other: PosBase) -> bool:
        raise NotImplementedError


class StrandStub(StrandBase):
    """
    Stub strand class. Hard-coded to track exactly
    four instances, which are mapped to hard-coded
    answer strands.
    """

    #
    # Class attributes
    #

    # StrandStub.counter tracks how many StrandStub
    # instances have been created
    counter = 0

    # StrandStub.positions{1,2,3,4} are hard-coded positions
    # corresponding to the four answer strands (CMSC, ONE, FORTY, TWO)
    positions1: list[PosBase] = [
        PosStub(0, 3),
        PosStub(0, 2),
        PosStub(0, 1),
        PosStub(0, 0),
    ]
    positions2: list[PosBase] = [PosStub(1, 0), PosStub(2, 0), PosStub(2, 1)]
    positions3: list[PosBase] = [
        PosStub(1, 1),
        PosStub(1, 2),
        PosStub(1, 3),
        PosStub(0, 4),
        PosStub(1, 4),
    ]
    positions4: list[PosBase] = [PosStub(2, 4), PosStub(2, 3), PosStub(2, 2)]

    all_positions: list[list[PosBase]] = [
        positions1,
        positions2,
        positions3,
        positions4,
    ]

    #
    # Instance attribute
    #

    strand_id: int

    def __init__(self, start: PosBase, steps: list[Step]):
        """
        Constructor

        The ith object to be constructed is assigned a
        strand_id of i.
        """
        self.start = start
        self.steps = steps
        self.strand_id = StrandStub.counter
        StrandStub.counter += 1

    def positions(self) -> list[PosBase]:
        """
        Return the hard-coded positions for the ith object.
        """
        return StrandStub.all_positions[self.strand_id]

    def is_cyclic(self) -> bool:
        """Not implemented"""
        raise NotImplementedError

    def is_folded(self) -> bool:
        """Not implemented"""
        raise NotImplementedError


class BoardStub(BoardBase):
    """
    Stub board class, hard-coded to assume a 3x5 board.
    """

    def __init__(self, letters: list[list[str]]):
        """Constructor"""
        self._letters = letters

    def num_rows(self) -> int:
        """Hard-coded to return 3"""
        return 3

    def num_cols(self) -> int:
        """Hard-coded to return 5"""
        return 5

    def get_letter(self, pos: PosBase) -> str:
        """Get letter at position. May raise IndexError."""
        return self._letters[pos.r][pos.c]

    def evaluate_strand(self, strand: StrandBase) -> str:
        """Not implemented"""
        raise NotImplementedError


class StrandsGameStub(StrandsGameBase):
    """
    Stub game logic. See module docstring at the top of file.
    """

    # Answers tracked in order from game file
    strands: list[StrandBase]

    # Found strands tracked in order of gameplay
    found: list[StrandBase]

    def __init__(self, filename: str, hint_threshold: int):
        """
        Constructor. See module docstring.
        """
        strand1 = StrandStub(PosStub(0, 3), [Step.W, Step.W, Step.W])
        strand2 = StrandStub(PosStub(1, 0), [Step.S, Step.E])
        strand3 = StrandStub(PosStub(1, 1), [Step.E, Step.E, Step.NE, Step.S])
        strand4 = StrandStub(PosStub(2, 4), [Step.W, Step.W])
        self.strands = [strand1, strand2, strand3, strand4]

        self.found = []

    def theme(self) -> str:
        """See module docstring"""
        return '"CS 142"'

    def board(self) -> BoardBase:
        """See module docstring"""
        return BoardStub(
            [
                [x for x in "CSMCT"],
                [x for x in "OFORY"],
                [x for x in "NEOWT"],
            ]
        )

    def answers(self) -> list[tuple[str, StrandBase]]:
        """See module docstring"""
        return [
            ("cmsc", self.strands[0]),
            ("one", self.strands[1]),
            ("forty", self.strands[2]),
            ("two", self.strands[3]),
        ]

    def found_strands(self) -> list[StrandBase]:
        """See module docstring"""
        return self.found

    def hint_threshold(self) -> int:
        """See module docstring"""
        return 0

    def hint_meter(self) -> int:
        """See module docstring"""
        return 0

    def active_hint(self) -> None | tuple[int, bool]:
        """See module docstring"""
        return None

    def game_over(self) -> bool:
        """See module docstring"""
        return False

    def submit_strand(self, strand: StrandBase) -> tuple[str, bool] | str:
        """See module docstring"""
        count = len(self.found)
        if count == 4:
            raise ValueError("Game is already over")
        else:
            next_strand = self.strands[count]
            self.found.append(next_strand)

        return ("BLAH", True)

    def use_hint(self) -> tuple[int, bool] | str:
        """See module docstring"""
        return "No hint for you. Next!"
