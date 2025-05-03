"""
Tests for Milestone 1 Game Logic
"""

import pytest

from base import BoardBase, PosBase, Step, StrandBase, StrandsGameBase
from fakes import BoardFake, Pos, StrandFake, StrandsGameFake


def test_your_confidence() -> None:
    """You got this!"""
    assert True


def test_your_inheritance() -> None:
    """Test required inheritance"""

    assert issubclass(Pos, PosBase), "Pos should inherit from PosBase"

    assert issubclass(
        StrandFake, StrandBase
    ), "StrandFake should inherit from StrandBase"

    assert issubclass(
        BoardFake, BoardBase
    ), "BoardFake should inherit from BoardBase"

    assert issubclass(
        StrandsGameFake, StrandsGameBase
    ), "StrandsGameFake should inherit from StrandsGameBase"


def test_pos_take_step() -> None:
    """Test stepping in eight neighboring directions"""
    pos = Pos(0, 0)
    assert pos.take_step(Step.N) == Pos(-1, 0)
    assert pos.take_step(Step.S) == Pos(1, 0)
    assert pos.take_step(Step.E) == Pos(0, 1)
    assert pos.take_step(Step.W) == Pos(0, -1)
    assert pos.take_step(Step.NW) == Pos(-1, -1)
    assert pos.take_step(Step.NE) == Pos(-1, 1)
    assert pos.take_step(Step.SW) == Pos(1, -1)
    assert pos.take_step(Step.SE) == Pos(1, 1)


def test_pos_take_step_again() -> None:
    """
    Test the same eight neighbors as in previous test,
    this time with some refactoring.
    """
    pos = Pos(0, 0)
    for step, expected in [
        (Step.N, Pos(-1, 0)),
        (Step.S, Pos(1, 0)),
        (Step.E, Pos(0, 1)),
        (Step.W, Pos(0, -1)),
        (Step.NW, Pos(-1, -1)),
        (Step.NE, Pos(-1, 1)),
        (Step.SW, Pos(1, -1)),
        (Step.SE, Pos(1, 1)),
    ]:
        assert pos.take_step(step) == expected


@pytest.mark.parametrize(
    "step, expected",
    [
        (Step.N, Pos(-1, 0)),
        (Step.S, Pos(1, 0)),
        (Step.E, Pos(0, 1)),
        (Step.W, Pos(0, -1)),
        (Step.NW, Pos(-1, -1)),
        (Step.NE, Pos(-1, 1)),
        (Step.SW, Pos(1, -1)),
        (Step.SE, Pos(1, 1)),
    ],
)
def test_pos_take_step_yet_again(step: Step, expected: PosBase) -> None:
    """
    Test the same eight neighbors as in previous tests,
    this time demonstrating how to use @pytest.mark.parametrize
    to turn it into eight separate tests for the purposes
    of accounting by pytest.
    """
    pos = Pos(0, 0)
    assert pos.take_step(step) == expected


def test_pos_step_to_1_away() -> None:
    """Test difference from eight neighbors"""
    pos = Pos(10, 5)
    for other_pos, expected in [
        (Pos(9, 5), Step.N),
        (Pos(11, 5), Step.S),
        (Pos(10, 6), Step.E),
        (Pos(10, 4), Step.W),
        (Pos(9, 4), Step.NW),
        (Pos(9, 6), Step.NE),
        (Pos(11, 4), Step.SW),
        (Pos(11, 6), Step.SE),
    ]:
        assert pos.step_to(other_pos) == expected


def test_pos_step_to_0_away() -> None:
    """Test difference from a position to itself"""
    pos = Pos(11, 5)

    with pytest.raises(ValueError):
        pos.step_to(pos)

    assert not pos.is_adjacent_to(pos)


def test_pos_step_to_2_away() -> None:
    """
    Test difference from a position to its "grand"
    neighbors, by which we mean the layer of positions
    that surrounds the square of eight neighbors.
    """
    pos = Pos(11, 5)
    num_grand_neighbors = 0

    for dr in [-2, 1, 0, 1, -2]:
        for dc in [-2, 1, 0, 1, -2]:
            if abs(dr) > 1 or abs(dc) > 1:
                num_grand_neighbors += 1
                pos2 = Pos(pos.r + dr, pos.c + dc)

                with pytest.raises(ValueError):
                    pos.step_to(pos2)

                assert not pos.is_adjacent_to(pos2)

    assert num_grand_neighbors == 16


def test_strand_positions_cs_142() -> None:
    """Test strands from boards/cs-142.txt"""

    strand1 = StrandFake(Pos(0, 3), [Step.W, Step.W, Step.W])
    strand2 = StrandFake(Pos(1, 0), [Step.S, Step.E])
    strand3 = StrandFake(Pos(1, 1), [Step.E, Step.E, Step.NE, Step.S])
    strand4 = StrandFake(Pos(2, 4), [Step.W, Step.W])

    positions1 = [Pos(0, 3), Pos(0, 2), Pos(0, 1), Pos(0, 0)]
    positions2 = [Pos(1, 0), Pos(2, 0), Pos(2, 1)]
    positions3 = [Pos(1, 1), Pos(1, 2), Pos(1, 3), Pos(0, 4), Pos(1, 4)]
    positions4 = [Pos(2, 4), Pos(2, 3), Pos(2, 2)]

    assert strand1.positions() == positions1, "CMSC strand"
    assert strand2.positions() == positions2, "ONE strand"
    assert strand3.positions() == positions3, "FORTY strand"
    assert strand4.positions() == positions4, "TWO strand"


def test_strand_positions_directions() -> None:
    """Test strands from boards/directions.txt"""

    strand1 = StrandFake(Pos(0, 0), [Step.E, Step.E, Step.E])
    strand2 = StrandFake(Pos(1, 3), [Step.W, Step.W, Step.W])
    strand3 = StrandFake(Pos(2, 0), [Step.S, Step.S, Step.S, Step.S])
    strand4 = StrandFake(Pos(6, 1), [Step.N, Step.N, Step.N, Step.N])
    strand5 = StrandFake(
        Pos(2, 2),
        [
            Step.S,
            Step.NE,
            Step.S,
            Step.S,
            Step.S,
            Step.NW,
            Step.S,
            Step.SE,
            Step.W,
        ],
    )

    def map_wrap(pairs: list[tuple[int, int]]) -> list[PosBase]:
        return [Pos(r, c) for r, c in pairs]

    positions1 = map_wrap([(0, 0), (0, 1), (0, 2), (0, 3)])
    positions2 = map_wrap([(1, 3), (1, 2), (1, 1), (1, 0)])
    positions3 = map_wrap([(2, 0), (3, 0), (4, 0), (5, 0), (6, 0)])
    positions4 = map_wrap([(6, 1), (5, 1), (4, 1), (3, 1), (2, 1)])
    positions5 = map_wrap(
        [
            (2, 2),
            (3, 2),
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3),
            (4, 2),
            (5, 2),
            (6, 3),
            (6, 2),
        ]
    )

    assert strand1.positions() == positions1, "east strand"
    assert strand2.positions() == positions2, "west strand"
    assert strand3.positions() == positions3, "south strand"
    assert strand4.positions() == positions4, "north strand"
    assert strand5.positions() == positions5, "directions strand"


def test_load_game_cs_142_txt_variations() -> None:
    """
    Test game files with differences in formatting of
    whitespace and in capitalization.
    """

    txt_variations = [
        """
        "CS 142"

        C S M C T
        O F O R Y
        N E O W T

        cmsc  1 4 w w w
        one   2 1 s e
        forty 2 2 e e ne s
        two   3 5 w w
        """,
        """
        "CS 142"

        C  S  M   C  T
        O  F  O   R   Y
        N  E  O   W    T

        cmsc  1 4 w w w
        one   2 1 s e
        forty 2 2 e e ne s
        two   3 5 w w
        """,
        """
        "CS 142"

        C S M C T
        O F O R Y
        N E O W T

        cmsc 1 4 w w w
        one 2 1 s e
        forty 2 2 e e ne s
        two 3 5 w w
        """,
        """
        "CS 142"

        C S M C T
        O F O R Y
        N E O W T

        cmsc 1 4     w  w w
            one 2 1 s     e
        forty 2 2   e e ne s
         two        3 5  w     w
        """,
        """
        "CS 142"

        C S M C t
        O f o r y
        N E O W T

        Cmsc  1 4 w w w
        ONE   2 1 s e
        foRTy 2 2 e e ne s
        two   3 5 w w
        """,
    ]

    answers = [
        ("cmsc", StrandFake(Pos(0, 3), [Step.W, Step.W, Step.W])),
        ("one", StrandFake(Pos(1, 0), [Step.S, Step.E])),
        ("forty", StrandFake(Pos(1, 1), [Step.E, Step.E, Step.NE, Step.S])),
        ("two", StrandFake(Pos(2, 4), [Step.W, Step.W])),
    ]

    for txt in txt_variations:
        # Split and remove the extra line from top
        # of the multi-line string literals above
        lines = txt.split("\n")
        lines = lines[1:]
        game = StrandsGameFake(lines)

        assert game.theme() == '"CS 142"'
        assert game.board().num_rows() == 3
        assert game.board().num_cols() == 5
        assert game.board().get_letter(Pos(0, 4)) == "t"
        assert game.answers() == answers
        assert len(game.found_strands()) == 0
        assert not game.game_over()


def test_play_game_cs_142_sequence_1() -> None:
    """
    Play all four answer strands one after another,
    in the order in which they appear in the game file.
    """
    game = StrandsGameFake("boards/cs-142.txt")

    assert game.submit_strand(StrandFake(Pos(0, 3), [])) == ("cmsc", True)
    assert len(game.found_strands()) == 1

    assert game.submit_strand(StrandFake(Pos(1, 0), [])) == ("one", True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(StrandFake(Pos(1, 1), [])) == ("forty", True)
    assert len(game.found_strands()) == 3

    assert game.submit_strand(StrandFake(Pos(2, 4), [])) == ("two", True)
    assert len(game.found_strands()) == 4

    assert game.game_over()


def test_play_game_cs_142_sequence_2() -> None:
    """
    Play all four answer strands in a different order.
    """
    game = StrandsGameFake("boards/cs-142.txt")

    assert game.submit_strand(StrandFake(Pos(1, 1), [])) == ("forty", True)
    assert game.submit_strand(StrandFake(Pos(2, 4), [])) == ("two", True)
    assert game.submit_strand(StrandFake(Pos(1, 0), [])) == ("one", True)
    assert game.submit_strand(StrandFake(Pos(0, 3), [])) == ("cmsc", True)

    assert game.game_over()


def test_play_game_cs_142_sequence_3() -> None:
    """
    Play some unsuccessful strands along the way.
    """
    game = StrandsGameFake("boards/cs-142.txt")

    assert game.submit_strand(StrandFake(Pos(1, 1), [])) == ("forty", True)
    assert game.submit_strand(StrandFake(Pos(2, 3), [])) == "Not a theme word"
    assert game.submit_strand(StrandFake(Pos(3, 2), [])) == "Not a theme word"
    assert game.submit_strand(StrandFake(Pos(1, 1), [])) == "Already found"
    assert len(game.found_strands()) == 1

    assert game.submit_strand(StrandFake(Pos(2, 4), [])) == ("two", True)
    assert game.submit_strand(StrandFake(Pos(1, 0), [])) == ("one", True)
    assert game.submit_strand(StrandFake(Pos(0, 1), [])) == "Not a theme word"
    assert len(game.found_strands()) == 3

    assert game.submit_strand(StrandFake(Pos(0, 3), [])) == ("cmsc", True)
    assert game.game_over()


def test_play_game_cs_142_sequence_4() -> None:
    """
    Play some hints along the way.
    """
    game = StrandsGameFake("boards/cs-142.txt")
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)
    assert game.submit_strand(StrandFake(Pos(0, 3), [])) == ("cmsc", True)
    assert game.submit_strand(StrandFake(Pos(1, 0), [])) == ("one", True)
    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)
    assert game.submit_strand(StrandFake(Pos(1, 1), [])) == ("forty", True)
    assert game.active_hint() is None
