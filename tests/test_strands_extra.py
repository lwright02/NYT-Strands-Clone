"""
Extra tests for Milestone 3 Game Logic
"""

import pytest
import os
from base import BoardBase, PosBase, Step, StrandBase, StrandsGameBase
from strands import Board, Pos, Strand, StrandsGame

def test_board_get_letter_and_evaluate_out_of_bounds() -> None:
    """
    get_letter and evaluate_strand should raise ValueError
    when any position falls off the board.
    """
    board = Board([['a', 'b'], ['c', 'd']])

    with pytest.raises(ValueError):
        board.get_letter(Pos(2, 0))
    with pytest.raises(ValueError):
        board.get_letter(Pos(0, 2))

    bad = Strand(Pos(1, 1), [Step.S, Step.S, Step.S, Step.S])
    with pytest.raises(ValueError):
        board.evaluate_strand(bad)


def test_submit_strand_off_board_raises() -> None:
    """
    submit_strand should propagate ValueError for a strand
    whose path steps off the board.
    """
    game = StrandsGame("boards/face-time.txt")

    bad = Strand(Pos(0, 0), [Step.N, Step.N, Step.N, Step.N])
    with pytest.raises(ValueError):
        game.submit_strand(bad)


def test_duplicate_dictionary_word_returns_false_each_time() -> None:
    """
    Non-theme dictionary words may be submitted repeatedly,
    and each time should return (word, False), not "Already found".
    """
    game = StrandsGame("boards/face-time.txt")

    cancer = Strand(Pos(1, 1), [Step.E, Step.NW, Step.W, Step.S, Step.S])
    first = game.submit_strand(cancer)
    assert first == ("cancer", False)
    second = game.submit_strand(cancer)
    assert second == ("cancer", False)


def test_use_hint_after_game_over_returns_consistent() -> None:
    """
    Once all theme answers have been found, use_hint()
    should always return "Use your current hint".
    """
    game = StrandsGame("boards/face-time.txt")

    for _, strand in game.answers():
        assert game.submit_strand(strand)[1] is True
    assert game.game_over()

    assert game.active_hint() is None

    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() is None


def test_constructor_case_insensitivity_on_list_input() -> None:
    """
    Constructor should accept mixed-case theme, board, and answer tokens,
    storing everything lowercase internally.
    """
    lines = [
        "TeStInG",
        "",
        "A B",
        "C D",
        "",
        "Cd 2 2 W N"
    ]
    game = StrandsGame(lines)

    assert game.theme() == "testing"

    assert len(game.answers()) == 1
    word, strand = game.answers()[0]
    assert word == "cd"

    assert strand.positions() == [Pos(1,1), Pos(1,0), Pos(0,0)]


def test_constructor_rejects_invalid_game_file_type() -> None:
    """
    Constructor must reject any game_file that's not a str or list[str].
    """
    with pytest.raises(ValueError):
        StrandsGame(123)

def test_hint_persists_if_unrelated_answer_solved(ft_game) -> None:
    """
    If you request a hint for answer #0 but then solve answer #1,
    the active hint for #0 remains in effect.
    """
    assert ft_game.use_hint() == (0, False)
    assert ft_game.active_hint() == (0, False)

    word1, strand1 = ft_game.answers()[1]
    assert ft_game.submit_strand(strand1) == (word1, True)

    assert ft_game.active_hint() == (0, False)


def test_full_hint_cycle_through_all_answers(ft_game) -> None:
    """
    Walk through EVERY answer in face-time.txt, calling use_hint()
    twice for each (interior then ends), without ever solving them.
    """
    n = len(ft_game.answers())

    for idx in range(n):
        assert ft_game.use_hint() == (idx, False)
        assert ft_game.use_hint() == (idx, True)
        assert ft_game.use_hint() == "Use your current hint"
        word, strand = ft_game.answers()[idx]
        ft_game.submit_strand(strand)


def test_hint_clears_and_advances_after_solving_current(dir_game) -> None:
    """
    After you reveal ends for answer-2, solving that same answer
    should clear active_hint and allow hints on answer-3.
    """
    dir_game.use_hint()  # (0, False)
    dir_game.use_hint()  # (0, True)
    word0, s0 = dir_game.answers()[0]
    dir_game.submit_strand(s0)

    dir_game.use_hint()  # (1, False)
    dir_game.use_hint()  # (1, True)
    word1, s1 = dir_game.answers()[1]
    dir_game.submit_strand(s1)

    assert dir_game.active_hint() is None
    assert dir_game.use_hint() == (2, False)
    assert dir_game.use_hint() == (2, True)

    word2, s2 = dir_game.answers()[2]
    dir_game.submit_strand(s2)
    assert dir_game.active_hint() is None

    assert dir_game.use_hint() == (3, False)


def test_scoring_face_time(ft_game) -> None:
    """
    Check that get_score() is updated correctly for:
      - non‐theme dictionary words (+5)
      - too short submissions (–2)
      - not-in-dictionary submissions (–2)
      - hint usage (–5)
      - theme word found (+10)
    """
    
    assert ft_game.get_score() == 0

    # 1) submit "food" (non-theme, in dictionary) → +5
    assert ft_game.submit_strand(Strand(Pos(6, 1), [Step.S, Step.E, Step.E])) == ("food", False)
    assert ft_game.get_score() == 5

    # 2) submit too‐short → –2
    assert ft_game.submit_strand(Strand(Pos(5, 1), [Step.N])) == "Too short"
    assert ft_game.get_score() == 3

    # 3) submit not in dictionary → –2
    assert ft_game.submit_strand(Strand(Pos(3, 2), [Step.W, Step.N, Step.W, Step.W])) == "Not in word list"
    assert ft_game.get_score() == 1

    # 4) submit "bronze" (second non-theme, in dictionary) → +5
    assert ft_game.submit_strand(
        Strand(Pos(1, 4), [Step.SE, Step.W, Step.NW, Step.NE, Step.E])
    ) == ("bronze", False)
    assert ft_game.get_score() == 6

    # 5) use a hint → –5
    assert ft_game.use_hint() == (0, False)
    assert ft_game.get_score() == 1

    # 6) finally submit a theme word → +10
    word0, strand0 = ft_game.answers()[0]
    assert ft_game.submit_strand(strand0) == (word0, True)
    assert ft_game.get_score() == 11