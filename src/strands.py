"""
Game logic for Milestone 2:
Pos, Strand, Board, StrandsGame
"""
import os
from typing import TypeAlias
from base import PosBase, StrandBase, BoardBase, StrandsGameBase, Step

Row: TypeAlias = int
Col: TypeAlias = int

STEPS: dict[Step, tuple[int, int]] = {
        Step.N: (-1, 0), Step.S: (1, 0), Step.E: (0, 1), Step.W: (0, -1),
        Step.NE: (-1, 1), Step.NW: (-1, -1), Step.SE: (1, 1), Step.SW: (1, -1)
        }

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
        row_dif: int
        col_dif: int
        row_dif, col_dif = STEPS[step]

        return Pos(self.r + row_dif, self.c + col_dif)

    def step_to(self, other: "Pos") -> Step:
        """
        See ABC docstring.
        """
        row_dif: int = other.r - self.r
        col_dif: int = other.c - self.c

        if row_dif == 0 and col_dif == 0:
            raise ValueError("Cannot test difference from a position to itself")

        for step, (r, c) in STEPS.items():
            if (row_dif, col_dif) == (r, c):
                return step

        raise ValueError("More than 1 Step Away")

    def is_adjacent_to(self, other: "Pos") -> bool:
        """
        See ABC docstring.
        """
        try:
            _ = self.step_to(other)
        except ValueError:
            return False
        return True

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
        pos: PosBase = self.start
        pos_seq: list[PosBase] = [pos]

        for step in self.steps:
            pos = pos.take_step(step)
            pos_seq.append(pos)

        return pos_seq

    def is_cyclic(self) -> bool:
        """
        See ABC docstring.
        """
        elts = self.positions()
        seen = set()

        for elt in elts:
            coord = (elt.r, elt.c)
            if coord in seen:
                return True
            seen.add(coord)

        return False

    def is_folded(self) -> bool:
        positions = self.positions()
        
        mids: list[tuple[float,float]] = []
        
        for i in range(len(positions)-1):
            a, b = positions[i], positions[i+1]
            mids.append(((a.r + b.r)/2, (a.c + b.c)/2))
        
        return len(mids) != len(set(mids))


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
        self.letters = letters
        
        correct_length = len(letters[0])
        for row in letters:
            if len(row) != correct_length:
                raise ValueError

    def num_rows(self) -> int:
        """
        Return the number of rows on the board.
        """
        return len(self.letters)

    def num_cols(self) -> int:
        """
        Return the number of columns on the board.
        """
        return len(self.letters[0])

    def get_letter(self, pos: PosBase) -> str:
        """
        Return the letter at a given position on the board.

        Raises ValueError if the position is not within the
        bounds of the board.
        """
        row: Row = pos.r
        col: Col = pos.c

        if row >= self.num_rows() or col >= self.num_cols():
            raise ValueError

        return self.letters[row][col]

    def evaluate_strand(self, strand: Strand) -> str:
        """
        See ABC docstring.
        """
        positions = strand.positions()
        result = []
        for elt in positions:
            if (0 <= elt.r < self.num_rows()) and (0 <= elt.c < self.num_cols()):
                result.append(self.get_letter(elt))
            else:
                raise ValueError

        return "".join(result)


######################################################################


class StrandsGame(StrandsGameBase):
    """
    Abstract base class for Strands game logic.
    """
    def __init__(self, game_file: str | list[str], hint_threshold: int = 3) -> None:
        """
        Constructor

        Load the game specified in a given file, and set
        a particular threshold for giving hints. The game
        file can be specified either as a string filename,
        or as the list of lines that result from calling
        readlines() on the file.

        Raises ValueError if the game file is invalid.

        Valid game files include:

          1. a theme followed by a single blank line, then

          2. multiple lines defining the board followed
             by a single blank line, then

          3. multiple lines defining the answers,
             optionally followed by

          4. a blank line and then any number of remaining
             lines which have no semantic meaning.

        Valid game files require:

          - boards to be rectangular

          - boards where each string is a single,
            alphabetical character (either upper- or
            lower case; for example, both "a" and "A"
            denote the same letter, which is stored
            as "a" in the board object)

          - each line for an answer of the form
            "WORD R C STEP1 STEP2 ..." where
              * WORD has at least three letters,
              * the position (R, C) is within bounds
                of the board,
              * the positions implied by the steps are
                all within bounds of the board, and
              * the letters implied by the strand
                spell the WORD (modulo capitalization)
              * the WORDs and STEPs may be spelled with
                either lower- or uppercase letters, but
                regardless the WORDs are stored in the
                game object with only lowercase letters.

           - that each answer strand has no folds
             (edges do not cross)

           - that answers fill the board

        Game files are allowed to use multiple space
        characters to separate tokens on a line. Also,
        leading and trailing whitespace will be ignored.
        """
        if isinstance(game_file, str):
            with open(game_file, 'r') as f:
                raw_lines = [line.rstrip('\n') for line in f]
        elif isinstance(game_file, list):
            raw_lines = [line.rstrip('\n') for line in game_file]
        else:
            raise ValueError("game_file must be a filename (str) or list[str]")

        lines: list[str] = []
        for ln in raw_lines:
            ln = ln.strip()
            if ln.lower().startswith("http"):
                break
            lines.append(ln)

        blank_idcs: list[int] = [i for i, ln in enumerate(lines) if ln == ""]
        if len(blank_idcs) < 2:
            raise ValueError("Invalid game file")
        first_blank: int = blank_idcs[0]
        second_blank: int = blank_idcs[1]

        theme_lines: list[str] = lines[0:first_blank]
        board_lines: list[str] = lines[(first_blank + 1):second_blank]
        answer_lines: list[str] = [ln for ln in lines[(second_blank + 1):] if ln]

        if not answer_lines:
            raise ValueError("No answers provided")
        
        self._theme: str = theme_lines[0]

        grid: list[list[str]] = []

        for row in board_lines:
            letters: list[str] = row.split()
            if len(letters) != len(board_lines[0].split()):
                raise ValueError("Invalid Strands Board (not rectangular)")
            grid.append([letter.lower() for letter in letters])

        self._board: Board = Board(grid)

        self._answers: list[tuple[str, StrandBase]] = []
        for line in answer_lines:
            sections: list[str] = line.split()
            word: str = sections[0].lower()

            r: int = int(sections[1]) - 1
            c: int = int(sections[2]) - 1

            steps: list[Step] = [Step(tok.lower()) for tok in sections[3:]]

            start: Pos = Pos(r, c)
            self._answers.append((word, Strand(start, steps)))

        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir)
        )
        
        dict_path = os.path.join(project_root, "assets", "web2.txt")
        
        with open(dict_path, "r") as dict_f:
            self._dictionary: set[str] = {
                w.strip().lower() for w in dict_f if w.strip()
            }

        self._found: list[StrandBase] = []
        self._hint_threshold: int = hint_threshold
        self._hint_meter: int = 0
        self._active_hint: tuple[int, bool] | None = None

    def theme(self) -> str:
        """
        Return the theme for the game.
        """
        return self._theme

    def board(self) -> Board:
        """
        Return the board for the game.
        """
        return self._board

    def answers(self) -> list[tuple[str, StrandBase]]:
        """
        Return the answers for the game. Each answer
        is a pair comprising a theme word and the
        corresponding strand on the board. Words are
        stored using lowercase letters, even if the
        game file used uppercase letters.
        """
        return self._answers

    def found_strands(self) -> list[StrandBase]:
        """
        Return the theme words that have been found so far,
        represented as strands. The order of strands in the
        output matches the order in which they were found.

        Note two strands may conflict, meaning they involve
        different sequences of steps yet identify the same
        absolute positions on the board. This method returns
        the strands that have been submitted through the
        user interface (i.e. submit_strand) and thus may
        deviate from the strands stored in answers.
        """
        return self._found

    def game_over(self) -> bool:
        """
        Decide whether or not the game is over, which means
        checking whether or not all theme words have been
        found.
        """
        for answer in self.answers():
            theme_word, strand = answer
            if strand not in self.found_strands():
                return False

        return True

    def hint_threshold(self) -> int:
        """
        Return the hint threshold for the game.
        """
        return self._hint_threshold

    def hint_meter(self) -> int:
        """
        Return the current hint meter for the game.
        If it is greater than or equal to the hint
        threshold, then the user can request a hint.
        """
        return self._hint_meter

    def active_hint(self) -> tuple[int, bool] | None:
        """
        Return the active hint, if any.

        Returns None:
            if there is no active hint.

        Returns (i, False):
            if the active hint corresponds to the ith answer
            in the list of answers, but the start and end
            positions _should not_ be shown to the user.

        Returns (i, True):
            if the active hint corresponds to the ith answer
            in the list of answers, and the start and end
            positions _should_ be shown to the user.
        """
        return self._active_hint

    def submit_strand(self, strand: StrandBase) -> tuple[str, bool] | str:
        """
        Play a selected strand.

        Returns (word, True):
            if the strand corresponds to a theme word which
            has not already been found.

        Returns (word, False):
            if the strand does not correspond to a theme
            word but does correspond to a valid dictionary
            word that has not already been found.

        Returns "Already found":
            if the strand corresponds to a theme word or
            dictionary word that has already been found.

        Returns "Too short":
            if the strand corresponds to fewer than four
            letters.

        Returns "Not in word list":
            if the strand corresponds to a string that
            is not a valid dictionary word.
        """
        positions = strand.positions()
        if len(positions) < 4:
            return "Too short"

        word = self._board.evaluate_strand(strand).lower()

        theme_set = {w for w, _ in self._answers}
        if word in theme_set:
            for idx, (w, answer_strand) in enumerate(self._answers):
                if w == word:
                    if answer_strand in self._found:
                        return "Already found"
                    
                    self._found.append(answer_strand)
                    if self._active_hint and self._active_hint[0] == idx:
                        self._active_hint = None
                    
                    return (w, True)
                
        if word not in self._dictionary:
            return "Not in word list"

        return (word, False)

    def use_hint(self) -> tuple[int, bool] | str:
        """
        Play a hint.

        Returns (i, b):
            if successfully updated the active hint. The new
            hint corresponds to the ith answer in the list of
            all answers, which is the first answer that has
            not already been found. The boolean b describes
            whether there was already an active hint before
            this call to use_hint (and thus whether or not the
            first and last letters of the hint word should be
            highlighted).

        Returns "No hint yet":
            if the current hint meter does not yet warrant
            a hint.

        Returns "Use your current hint":
            if there is already an active hint where the
            first and last letters are being displayed.
        """
        if self._active_hint is None:
            for idx, (_, answer) in enumerate(self._answers):
                if answer not in self._found:
                    self._active_hint = (idx, False)
                    return self._active_hint

            return "Use your current hint"

        idx, shown_end = self._active_hint
        if not shown_end:
            self._active_hint = (idx, True)
            return self._active_hint

        return "Use your current hint"