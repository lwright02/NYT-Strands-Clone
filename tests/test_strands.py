"""
Tests for Milestone 2 Game Logic
"""

import pytest

from base import BoardBase, PosBase, Step, StrandBase, StrandsGameBase
from strands import Board, Pos, Strand, StrandsGame

eight_neighbors = [
    (Step.N,  Pos(2, 2)),
    (Step.S,  Pos(4, 2)),
    (Step.E,  Pos(3, 3)),
    (Step.W,  Pos(3, 1)),
    (Step.NW, Pos(2, 1)),
    (Step.NE, Pos(2, 3)),
    (Step.SW, Pos(4, 1)),
    (Step.SE, Pos(4, 3)),
]

cardinals = [Step.N, Step.S, Step.E, Step.W]
intercardinals = [Step.NW, Step.NE, Step.SW, Step.SE]

def test_inheritance() -> None:
    """Test required inheritance"""

    assert issubclass(Pos, PosBase), "Pos should inherit from PosBase"

    assert issubclass(
        Strand, StrandBase
    ), "Strand should inherit from StrandBase"

    assert issubclass(
        Board, BoardBase
    ), "Board should inherit from BoardBase"

    assert issubclass(
        StrandsGame, StrandsGameBase
    ), "StrandsGame should inherit from StrandsGameBase"


def test_pos_take_step() -> None:
    """
    Test stepping in eight neighboring directions
    """
    pos = Pos(3, 2)
    for step, expected in eight_neighbors:
        assert pos.take_step(step) == expected


def test_pos_step_to_success() -> None:
    """Test differences from eight neighbors"""
    pos = Pos(3, 2)
    for step, expected in eight_neighbors:
        assert pos.step_to(expected) == step


def test_pos_step_to_failure() -> None:
    """Test differences from positions two and three steps away"""
    pos = Pos(3, 2)
    
    two_step_apart = [
    Pos(5, 2),
    Pos(3, 4),
    Pos(5, 4),
    Pos(1, 3), 
    ]

    three_step_apart = [
    Pos(0, 2),
    Pos(1, 3),
    Pos(3, 5),
    Pos(3, -1), 
    ]
    
    for other in two_step_apart + three_step_apart:
        with pytest.raises(ValueError):
            pos.step_to(other)

        assert not pos.is_adjacent_to(other)

def test_strand_positions_straight_cardinal() -> None:
    """
    Create four strands, one in each cardinal direction, 
    each with at least four steps, and check that the 
    positions method returns the expected path.
    """
    start = Pos(3, 2)
    steps_dict = {
        Step.N: [(2, 2), (1, 2), (0, 2)],
        Step.S: [(4, 2), (5, 2), (6, 2)],
        Step.E: [(3, 3), (3, 4), (3, 5)],
        Step.W: [(3, 1), (3, 0), (3, -1)],
    }

    for step, coords in steps_dict.items():
        strand = Strand(start, [step] * 3)
        expected_positions = [start] + [Pos(r, c) for (r, c) in coords]
        assert strand.positions() == expected_positions


def test_strand_positions_straight_intercardinal() -> None:
    """
    Create four strands, one in each intercardinal direction, 
    each with at least four steps, and check that the 
    positions method returns the expected path.
    """
    start = Pos(3, 2)
    steps_dict = {
        Step.NE: [(2, 3), (1, 4), (0, 5)],
        Step.NW: [(2, 1), (1, 0), (0, -1)],
        Step.SE: [(4, 3), (5, 4), (6, 5)],
        Step.SW: [(4, 1), (5, 0), (6, -1)],
    }

    for step, coords in steps_dict.items():
        strand = Strand(start, [step] * 3)
        expected_positions = [start] + [Pos(r, c) for (r, c) in coords]
        assert strand.positions() == expected_positions

def test_strand_positions_long() -> None:
    """
    Create two long strands:
    - One with steps in all eight directions that does NOT fold.
    - One that folds (crosses over itself).
    """
    start = Pos(3, 2)

    steps_non_folded = [
        Step.E, Step.SE, Step.S, Step.SW,
        Step.W, Step.NW, Step.N, Step.NE
    ]
    strand1 = Strand(start, steps_non_folded)
    positions1 = strand1.positions()
    
    assert len(set(positions1)) == len(positions1)
    assert not strand1.is_folded()

    steps_folded = [Step.E, Step.S, Step.W, Step.N, Step.NE, Step.S, Step.E]
    strand2 = Strand(start, steps_folded)
    positions2 = strand2.positions()
    
    assert len(set(positions2)) != len(positions2)
    assert strand2.is_folded()

def test_load_game_face_time_file() -> None:
    """
    Load the official face_time.txt file and check basic values.
    """
    game = StrandsGame("boards/face_time.txt")

    assert game.theme() == "Face time"
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6
    assert len(game.answers()) > 0

def test_load_game_face_time_variations() -> None:
    """
    Load the same game using a list of strings instead of a file,
    and check that it still works.
    """
    with open("boards/face_time.txt") as f:
        lines = f.readlines()

    game = StrandsGame(lines)

    assert game.theme() == "Face time"
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6
    assert len(game.answers()) > 0

def test_load_game_face_time_invalid() -> None:
    """
    Try loading invalid game files and confirm ValueError is raised.
    """

    # Board is not rectangular
    broken_board = [
        '"Face time"', "",
        "A B C D",     # 4 columns
        "E F G",       # 3 columns – invalid
        "",            # blank line
        "primer 1 1 e e e",  # not relevant
    ]
    with pytest.raises(ValueError):
        StrandsGame(broken_board)

    # Empty answer line (sections[0] will fail)
    bad_answer = [
        '"Face time"', "",
        "A B C", "D E F", "",
        "",  # empty answer line (or just "   ")
    ]
    with pytest.raises(IndexError):
        StrandsGame(bad_answer)

def test_play_game_face_time_once() -> None:
    """
    Submit theme words in order and check progress.
    """
    game = StrandsGame("boards/face_time.txt")

    # Submit primer
    result1 = game.submit_strand(Strand(Pos(3, 3), []))
    assert result1 == ("primer", True)

    # Submit powder
    result2 = game.submit_strand(Strand(Pos(6, 2), []))
    assert result2 == ("powder", True)

    # Already found
    result3 = game.submit_strand(Strand(Pos(3, 3), []))
    assert result3 == "Already found"

def test_play_game_face_time_twice() -> None:
    """
    Submit same answers as previous test but out of order.
    """
    game = StrandsGame("boards/face_time.txt")

    # Submit powder first
    result1 = game.submit_strand(Strand(Pos(6, 2), []))
    assert result1 == ("powder", True)

    # Submit primer next
    result2 = game.submit_strand(Strand(Pos(3, 3), []))
    assert result2 == ("primer", True)

def test_play_game_face_time_three_times() -> None:
    """
    Submit a theme word, then a non-theme word,
    then repeat the original word again.
    """
    game = StrandsGame("boards/face_time.txt")

    # Submit primer correctly
    assert game.submit_strand(Strand(Pos(3, 3), [])) == ("primer", True)

    # Submit invalid strand (not a theme word)
    assert game.submit_strand(Strand(Pos(0, 0), [])) == "Not a theme word"

    # Submit the same correct word again
    assert game.submit_strand(Strand(Pos(3, 3), [])) == "Already found"

def test_play_game_face_time_more() -> None:
    """
    Trigger each of the use_hint stages.
    """
    game = StrandsGame("boards/face_time.txt")

    # Hint before anything found: should return index 0 with show=False
    assert game.use_hint() == (0, False)

    # Use it again: now it should show start/end
    assert game.use_hint() == (0, True)

    # Use it again: still active, already showing, so no change
    assert game.use_hint() == "Use your current hint"

    # Submit the hint's word: primer at (4, 4) -> Pos(3, 3)
    assert game.submit_strand(Strand(Pos(3, 3), [])) == ("primer", True)

    # Hint now should reset; call use_hint again to get the next one
    assert game.use_hint() == (1, False)
