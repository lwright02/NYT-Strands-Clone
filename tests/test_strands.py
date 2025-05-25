"""
Tests for Milestone 3 Game Logic
"""

import pytest
import os
from base import BoardBase, PosBase, Step, StrandBase, StrandsGameBase
from strands import Board, Pos, Strand, StrandsGame

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

@pytest.mark.parametrize("step, expected", eight_neighbors)
def test_pos_take_step(step, expected) -> None:
    """
    Test stepping in eight neighboring directions
    """
    pos = Pos(3, 2)
    assert pos.take_step(step) == expected


@pytest.mark.parametrize("step, expected", eight_neighbors)
def test_pos_step_to_success(step, expected) -> None:
    """Test differences from eight neighbors"""
    pos = Pos(3, 2)
    assert pos.step_to(expected) == step


two_steps_apart = [
    Pos(5, 2),
    Pos(3, 4),
    Pos(5, 4),
    Pos(1, 3), 
]

three_steps_apart = [
    Pos(0, 2),
    Pos(1, 3),
    Pos(3, 5),
    Pos(3, -1), 
]

@pytest.mark.parametrize("other", two_steps_apart + three_steps_apart)
def test_pos_step_to_failure(other) -> None:
    """Test differences from positions two and three steps away"""
    pos = Pos(3, 2)
    
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
        Step.N: [(2, 2), (1, 2), (0, 2), (-1, 2)],
        Step.S: [(4, 2), (5, 2), (6, 2), (7, 2)],
        Step.E: [(3, 3), (3, 4), (3, 5), (3, 6)],
        Step.W: [(3, 1), (3, 0), (3, -1), (3, -2)],
    }

    for step, coords in steps_dict.items():
        strand = Strand(start, [step] * 4)
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
        Step.NE: [(2, 3), (1, 4), (0, 5), (-1, 6)],
        Step.NW: [(2, 1), (1, 0), (0, -1), (-1, -2)],
        Step.SE: [(4, 3), (5, 4), (6, 5), (7, 6)],
        Step.SW: [(4, 1), (5, 0), (6, -1), (7, -2)],
    }

    for step, coords in steps_dict.items():
        strand = Strand(start, [step] * 4)
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
    
    assert positions1 == [Pos(3,2), Pos(3,3), Pos(4,4), Pos(5,4), Pos(6,3),
                          Pos(6,2), Pos(5,1), Pos(4,1), Pos(3,2)]
    assert not strand1.is_folded()

    steps_folded = [Step.SE, Step.N, Step.SW, Step.N, Step.E, Step.E, Step.S]
    strand2 = Strand(start, steps_folded)
    positions2 = strand2.positions()
    
    assert positions2 == [Pos(3,2), Pos(4,3), Pos(3,3), Pos(4,2), Pos(3,2),
                          Pos(3,3), Pos(3,4), Pos(4,4)]
    assert strand2.is_folded()

def test_load_game_face_time_file() -> None:
    """
    Load the official face-time.txt file and check basic values.
    """
    game = StrandsGame("boards/face-time.txt")

    assert game.theme() == '"Face time"'
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6
    assert len(game.answers()) == 6

def test_load_game_face_time_variations() -> None:
    """
    Load the same game using a list of strings instead of a file,
    and check that it still works.
    """
    with open("boards/face-time.txt") as f:
        lines = f.readlines()

    game = StrandsGame(lines)

    assert game.theme() == '"face time"'
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6
    assert len(game.answers()) == 6

invalid_boards_face_time = [
    (
        [
            '"Face time"', "",
            "A B C D",
            "E F G",
            "",
            "primer 1 1 e e e",
        ],
        ValueError
    ),
    (
        [
            '"Face time"', "",
            "A B C", "D E F", "",
            "",
        ],
        ValueError
    ),
]

@pytest.mark.parametrize("board, error", invalid_boards_face_time)
def test_load_game_face_time_invalid(board, error) -> None:
    """
    Try loading invalid game files and confirm the expected
    errors are raised.
    """
    with pytest.raises(error):
        StrandsGame(board)


def play_game_once_helper(game):
    """
    Helper function that plays answer strands in the
    order in which they appear in the game file.
    """
    length = 0
    for word, correct_strand in game.answers():
        length += 1
        assert game.submit_strand(correct_strand) == (word, True)
        assert len(game.found_strands()) == length
    assert game.game_over()

def play_game_twice_helper(game):
    """
    Helper function that plays answer strands in the
    reverse order in which they appear in the game file.
    """
    for word, correct_strand in game.answers()[::-1]:
        assert game.submit_strand(correct_strand) == (word, True)
    assert game.game_over()

def play_game_more_helper(game):
    """
    Helper function providing logic to trigger each 
    of the use_hint stages.
    """
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)

    assert game.use_hint() == (0, True)
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)

    word, strand = game.answers()[0]
    assert game.submit_strand(strand) == (word, True)
    assert game.use_hint() == (1, False)

    word, strand = game.answers()[2]
    assert game.submit_strand(strand) == (word, True)
    assert game.use_hint() == (1, True)

    word, strand = game.answers()[1]
    assert game.submit_strand(strand) == (word, True)
    assert game.active_hint() == None

def test_play_game_face_time_once(ft_game) -> None:
    """
    Play all four answer strands one after another,
    in the order in which they appear in the game file.
    """
    play_game_once_helper(ft_game)

def test_play_game_face_time_twice(ft_game) -> None:
    """
    Submit same answers as previous test but out of order.
    """
    play_game_twice_helper(ft_game)


def test_play_game_face_time_three_times(ft_game) -> None:
    """
    Play some unsuccessful strands along the way.
    """
    assert ft_game.submit_strand(ft_game.answers()[5][1]) == ("makeupexam", True)
    assert ft_game.submit_strand(ft_game.answers()[2][1]) == ("bronzer", True)
    assert ft_game.submit_strand(
    Strand(Pos(1, 1), [Step.E, Step.NW, Step.W, Step.S, Step.S])
    ) == ("cancer", False)

    assert ft_game.submit_strand(
    Strand(Pos(3, 2), [Step.W, Step.N, Step.W, Step.S])
    ) == "Not in word list"
    assert ft_game.submit_strand(ft_game.answers()[5][1]) == "Already found"
    assert len(ft_game.found_strands()) == 2

    assert ft_game.submit_strand(ft_game.answers()[3][1]) == ("concealer", True)
    assert ft_game.submit_strand(ft_game.answers()[4][1]) == ("foundation", True)
    assert ft_game.submit_strand(
    Strand(Pos(5, 1), [Step.N, Step.E])
    ) == "Too short"
    assert len(ft_game.found_strands()) == 4

    assert ft_game.submit_strand(ft_game.answers()[3][1]) == "Already found"
    assert ft_game.submit_strand(ft_game.answers()[0][1]) == ("primer", True)
    assert ft_game.submit_strand(ft_game.answers()[1][1]) == ("powder", True)

    assert ft_game.game_over()

def test_play_game_face_time_more(ft_game) -> None:
    """
    Trigger each of the use_hint stages.
    """
    play_game_more_helper(ft_game)

cyclic_strands = [
    (Strand(Pos(0,0), [Step.E, Step.S, Step.W, Step.N]), True), 
    (Strand(Pos(0,0), [Step.N, Step.N, Step.E, Step.S, Step.W, Step.W]), True), 
    (Strand(Pos(0,0), [Step.NE, Step.W, Step.S, Step.S, Step.NE, Step.W]), True), 
    (Strand(Pos(0,0), [Step.E, Step. E, Step.W]), True)
]

@pytest.mark.parametrize("strand, expected", cyclic_strands)
def test_is_cyclic(strand, expected) -> None:
    """
    Check that is_cyclic returns the appropriate answer
    for four acylic strands.
    """
    assert strand.is_cyclic() == expected

acyclic_strands = [
    (Strand(Pos(0,0), [Step.E, Step.S, Step.E, Step.N]), False), 
    (Strand(Pos(0,0), [Step.N, Step.W, Step.S, Step.S, Step.S, Step.E]), False), 
    (Strand(Pos(0,0), [Step.NE, Step.S, Step.SW, Step.W]), False), 
    (Strand(Pos(0,0), [Step.E, Step.E, Step.E, Step.E, Step.E]), False)
]

@pytest.mark.parametrize("strand, expected", acyclic_strands)
def test_is_not_cyclic(strand, expected) -> None:
    """
    Check that is_cyclic returns the appropriate answer
    for four acylic strands.
    """
    assert strand.is_cyclic() == expected

def test_overlapping() -> None:
    """
    """
    game1 = StrandsGame("boards/i-get-around.txt")
    
    # First valid path for "wheelie"
    assert game1.submit_strand(
    Strand(Pos(5,0), [Step.E, Step.E, Step.N, Step.SE, Step.E, Step.E])
    ) == ("wheelie", True) 

    # Second valid path for "wheelie"
    assert game1.submit_strand(
    Strand(Pos(5,0), [Step.E, Step.NE, Step.S, Step.E, Step.E, Step.E])
    ) == "Already found"

    game2 = StrandsGame("boards/what-a-trill.txt")
    
    # First valid path for "sparrow"
    assert game2.submit_strand(
    Strand(Pos(1,3), [Step.NE, Step.E, Step.S, Step.W, Step.S, Step.W])
    ) == ("sparrow", True)

    # Second valid path for "sparrow"
    assert game2.submit_strand(
    Strand(Pos(1,3), [Step.NE, Step.E, Step.SW, Step.E, Step.SW, Step.W])
    ) == "Already found"

def test_load_game_directions_file() -> None:
    """
    Load the official face_time.txt file and check basic values.
    """
    game = StrandsGame("boards/directions.txt")

    assert game.theme() == '"Directions"'
    assert game.board().num_rows() == 7
    assert game.board().num_cols() == 4
    assert len(game.answers()) == 5

def test_load_game_directions_variations() -> None:
    """
    Load the same game using a list of strings instead of a file,
    and check that it still works.
    """
    with open("boards/directions.txt") as f:
        lines = f.readlines()

    game = StrandsGame(lines)

    assert game.theme() == '"directions"'
    assert game.board().num_rows() == 7
    assert game.board().num_cols() == 4
    assert len(game.answers()) == 5

invalid_boards_directions = [
    (
        # Irregular grid (one row has only 3 letters instead of 4) ⇒ ValueError
        [
            '"Directions"',
            "",
            "E A S T",
            "T S E W",
            "S H D",        # <-- too short
            "O T I E",
            "U R I C",
            "T O O T",
            "H N S N",
            "",
            # answers (would be valid if the grid were okay)
            "east 1 1 e e e",
            "west 2 4 w w w",
            "south 3 1 s s s s",
            "north 7 2 n n n n",
            "directions 3 3 s ne s s s nw s se w",
        ],
        ValueError
    ),
    (
        # Missing any answer lines ⇒ IndexError
        [
            '"Directions"',
            "",
            "E A S T",
            "T S E W",
            "S H D R",
            "O T I E",
            "U R I C",
            "T O O T",
            "H N S N",
            "",
            "",   # blank line for answers, but no answers follow
        ],
        ValueError
    ),
]

@pytest.mark.parametrize("board, error", invalid_boards_directions)
def test_load_game_directions_invalid(board, error) -> None:
    """
    Try loading invalid 'Directions' game files and
    confirm the expected errors are raised.
    """
    with pytest.raises(error):
        StrandsGame(board)


def test_play_game_directions_once(dir_game) -> None:
    """
    Play all four answer strands one after another,
    in the order in which they appear in the "directions"
    game file.
    """
    play_game_once_helper(dir_game)

def test_play_game_directions_twice(dir_game) -> None:
    """
    Submit same answers as previous test but out of order.
    """
    play_game_twice_helper(dir_game)


def test_play_game_directions_three_times(dir_game) -> None:
    """
    Play some unsuccessful strands along the way.
    """
    assert dir_game.submit_strand(dir_game.answers()[4][1]) == ("directions", True)
    assert dir_game.submit_strand(dir_game.answers()[2][1]) == ("south", True)
    assert dir_game.submit_strand(
    Strand(Pos(2, 0), [Step.S, Step.S, Step.E])
    ) == ("sour", False)

    assert dir_game.submit_strand(
    Strand(Pos(1, 1), [Step.S, Step.SW, Step.NE, Step.W])
    ) == "Not in word list"
    assert dir_game.submit_strand(dir_game.answers()[4][1]) == "Already found"
    assert len(dir_game.found_strands()) == 2

    assert dir_game.submit_strand(dir_game.answers()[3][1]) == ("north", True)
    assert dir_game.submit_strand(dir_game.answers()[1][1]) == ("west", True)
    assert dir_game.submit_strand(
    Strand(Pos(4, 1), [Step.E, Step.SW])
    ) == "Too short"
    assert len(dir_game.found_strands()) == 4

    assert dir_game.submit_strand(dir_game.answers()[3][1]) == "Already found"
    assert dir_game.submit_strand(dir_game.answers()[0][1]) == ("east", True)

    assert dir_game.game_over()

def test_play_game_directions_more(dir_game) -> None:
    """
    Trigger each of the use_hint stages with the
    "directions" game file.
    """
    play_game_more_helper(dir_game)


HERE = os.path.dirname(__file__)
BOARD_DIR = os.path.abspath(os.path.join(HERE, os.pardir, "boards"))

board_files = [
    os.path.join(BOARD_DIR, fname)
    for fname in os.listdir(BOARD_DIR)
]

@pytest.mark.parametrize("filename", board_files)
def test_valid_game_files(filename) -> None:
    """
    Test the validity of each game file in the boards/
    directory.
    """
    game = StrandsGame(filename)


def play_game_hints_0_helper(game) -> None:
    """
    Helper function that drives a game with hint
    threshold zero into a state where use_hint is 
    successful five times
    """
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)

    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)

    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)

    word, strand = game.answers()[0]
    assert game.submit_strand(strand) == (word, True)
    assert game.active_hint() is None

    assert game.use_hint() == (1, False)
    assert game.active_hint() == (1, False)

    assert game.use_hint() == (1, True)
    assert game.active_hint() == (1, True)


def test_play_game_face_time_hints_0() -> None:
    """
    Trigger five succesful uses of use_hint with the
    "face time" game file and a hint threshold of zero.
    """
    ft_game = StrandsGame("boards/face-time.txt", 0)
    play_game_hints_0_helper(ft_game)


def test_play_game_face_time_hints_1() -> None:
    """
    Trigger four succesful uses of use_hint with the
    "face time" game file and a hint threshold of one.
    """
    ft_game = StrandsGame("boards/face-time.txt", 1)
    
    assert ft_game.submit_strand(
        Strand(Pos(6, 1), [Step.S, Step.E, Step.E])
    ) == ("food", False)
    assert ft_game.use_hint() == (0, False)
    assert ft_game.active_hint() == (0, False)

    assert ft_game.submit_strand(
        Strand(Pos(1, 4), [Step.SE, Step.W, Step.NW, Step.NE, Step.E, Step.S])
    ) == ("bronze", False)
    assert ft_game.use_hint() == (0, True)
    assert ft_game.active_hint() == (0, True)

    word, strand = ft_game.answers()[0]
    assert ft_game.submit_strand(strand) == (word, True)

    assert ft_game.submit_strand(
        Strand(Pos(2, 0), [Step.E, Step.N, Step.W])
    ) == ("race", False)
    assert ft_game.use_hint() == (1, False)
    assert ft_game.active_hint() == (1, False)

    assert ft_game.submit_strand(
        Strand(Pos(1, 1), [Step.E, Step.NW, Step.W, Step.S, Step.S])
    ) == ("cancer", False)
    assert ft_game.use_hint() == (1, True)
    assert ft_game.active_hint() == (1, True)

def test_play_game_directions_hints_0() -> None:
    """
    Trigger five succesful uses of use_hint with the
    "directions" game file and a hint threshold of zero.
    """
    dir_game = StrandsGame("boards/directions.txt", 0)
    play_game_hints_0_helper(dir_game)

def test_play_game_face_time_hints_1() -> None:
    """
    Trigger four succesful uses of use_hint with the
    "directions" game file and a hint threshold of one.
    """
    dir_game = StrandsGame("boards/directions.txt", 1)
    
    assert dir_game.submit_strand(
    Strand(Pos(2, 0), [Step.E, Step.SW, Step.S, Step.NE])
    ) == ("shout", False)
    assert dir_game.use_hint() == (0, False)
    assert dir_game.active_hint() == (0, False)
    
    assert dir_game.submit_strand(
    Strand(Pos(6, 2), [Step.W, Step.N, Step.NW, Step.S])
    ) == ("snout", False)
    assert dir_game.use_hint() == (0, True)
    assert dir_game.active_hint() == (0, True)

    word, strand = dir_game.answers()[0]
    assert dir_game.submit_strand(strand) == (word, True)

    assert dir_game.submit_strand(
    Strand(Pos(4, 1), [Step.E, Step.E, Step.N])
    ) == ("rice", False)
    assert dir_game.use_hint() == (1, False)
    assert dir_game.active_hint() == (1, False)

    assert dir_game.submit_strand(
    Strand(Pos(2, 0), [Step.S, Step.S, Step.E])
    ) == ("sour", False)
    assert dir_game.use_hint() == (1, True)
    assert dir_game.active_hint() == (1, True)
