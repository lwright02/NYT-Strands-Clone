"""
GUI for Strands
"""

import pygame
import sys
from fakes import Pos, StrandFake, BoardFake, StrandsGameFake
from stubs import PosStub, StrandStub, BoardStub, StrandsGameStub
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase

COLORS: dict[str, tuple[int, int, int]] = {
    "WHITE": (255, 255, 255), "YELLOW": (255, 255, 0), "BLACK": (0, 0, 0)
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
    surface_width = CELL_SIZE * cols
    surface_height = CELL_SIZE * (rows + 1)
    font = pygame.font.SysFont(None, 36)    

    for row in range(rows):
        for col in range(cols):
            position = PosStub(row, col)
            letter = board.get_letter(position)
            rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(surface, COLORS["YELLOW"], rect, width = 2)
            letter_surface = font.render(letter, True, COLORS["BLACK"])
            letter_rect = letter_surface.get_rect(center = (
                col * CELL_SIZE + CELL_SIZE // 2, 
                row * CELL_SIZE + CELL_SIZE // 2)
                )
            surface.blit(letter_surface, letter_rect)
    
    hint_surface = font.render("Found 0/4 Use Hint", True, COLORS["BLACK"])
    hint_rect = hint_surface.get_rect(center = (
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
    board = game.board()
    rows: int = board.num_rows()
    cols: int = board.num_cols()
    surface_width = CELL_SIZE * cols
    surface_height = CELL_SIZE * (rows + 1)
    surface = pygame.display.set_mode((surface_width, surface_height))
    clock = pygame.time.Clock()

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

        refresh_board(surface, game)
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    run_game()