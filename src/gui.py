"""
GUI for Strands
"""

import pygame
import sys
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake
from stubs import PosStub, StrandStub, BoardStub, StrandsGameStub
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase

COLORS: dict[str, tuple[int, int, int]] = {
    "WHITE": (255, 255, 255), "YELLOW": (255, 255, 0), "BLACK": (0, 0, 0), 
    "LIGHTBLUE": (170, 215, 230)
    }
CELL_SIZE: int = 50


def refresh_board(surface: pygame.surface.Surface, strands: StrandsGameBase) -> None:
    """
    Draws the current state of the Board
    """
    surface.fill((COLORS["WHITE"]))
    board: BoardBase = strands.board()
    rows: int = board.num_rows()
    cols: int = board.num_cols()
    surface_width: int = CELL_SIZE * cols
    surface_height: int = CELL_SIZE * (rows + 1)
    font: pygame.font.Font = pygame.font.SysFont(None, 36)

    # Creates a set of positions for the found words and adds the lines between
    # the positions
    highlighted_positions: set[tuple[int, int]] = set()
    for word in strands.found_strands():
        positions: list[PosBase] = word.positions()
        if len(positions) >= 2:
            for i in range(len(positions) - 1):
                pos_1: PosBase = positions[i]
                pos_2: PosBase = positions[i + 1]
                x1: int = pos_1.c * CELL_SIZE + CELL_SIZE // 2
                y1: int = pos_1.r * CELL_SIZE + CELL_SIZE // 2
                x2: int = pos_2.c * CELL_SIZE + CELL_SIZE // 2
                y2: int = pos_2.r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(surface, COLORS["LIGHTBLUE"], (x1, y1), 
                    (x2, y2), width=4)
        for pos in positions:
            highlighted_positions.add((pos.r, pos.c))

    # Adds/Updates the letters on the surface as well as blue circles for words
    # that are already found
    for row in range(rows):
        for col in range(cols):
            position: PosBase = PosStub(row, col)
            letter: str = board.get_letter(position)

            if (row, col) in highlighted_positions:
                center: tuple[int, int] = (col * CELL_SIZE + CELL_SIZE // 2, 
                    row * CELL_SIZE + CELL_SIZE // 2)
                radius: int = CELL_SIZE // 3
                pygame.draw.circle(surface, COLORS["LIGHTBLUE"], center, radius)

            letter_surface: pygame.Surface = font.render(letter, True, 
                COLORS["BLACK"])
            letter_rect: pygame.Rect = letter_surface.get_rect(center = (
                col * CELL_SIZE + CELL_SIZE // 2, 
                row * CELL_SIZE + CELL_SIZE // 2)
                )
            surface.blit(letter_surface, letter_rect)
    
    # Adds/Updates the "found" phrase on the bottom
    hint_surface: pygame.Surface = font.render(f"Found {len(
        strands.found_strands())}/{len(strands.answers())} Use Hint", True, 
        COLORS["BLACK"])
    hint_rect: pygame.Rect = hint_surface.get_rect(center = (
        surface_width //2, 
        surface_height - (0.5 * CELL_SIZE))
        )
    surface.blit(hint_surface, hint_rect)


def run_game() -> None:
    """
    Plays a game of Strands on a pygame window
    """
    pygame.init()
    pygame.display.set_caption("Strands")
    game: StrandsGameBase = StrandsGameStub("filename", hint_threshold = 3)
    board: BoardBase = game.board()
    rows: int = board.num_rows()
    cols: int = board.num_cols()
    surface_width: int = CELL_SIZE * cols
    surface_height: int = CELL_SIZE * (rows + 1)
    surface: pygame.Surface = pygame.display.set_mode((surface_width, 
        surface_height))
    clock: pygame.time.Clock = pygame.time.Clock()
    answers: list[tuple[str, StrandBase]] = game.answers()
    i: int = 0

    while not game.game_over():

        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:
                    game.submit_strand(answers[i][1])
                    i += 1

        refresh_board(surface, game)
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    run_game()
