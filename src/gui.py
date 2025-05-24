"""
GUI for Strands
"""

import click, random, os, pygame, sys, math
from strands import Pos, Strand, StrandsGame
from base import Step, PosBase, StrandBase, BoardBase, StrandsGameBase
from ui import ArtGUIStub, ArtGUIBase
from art_gui import ArtGUI9Slice, ArtGUICat3, ArtGUICat4

COLORS: dict[str, tuple[int, int, int]] = {
    "WHITE": (255, 255, 255), 
    "YELLOW": (255, 255, 0), 
    "BLACK": (0, 0, 0), 
    "LIGHTBLUE": (170, 215, 230), 
    "GREEN": (0, 255, 0),
    "PINK": (255, 180, 190)
    }
CELL_SIZE: int = 50

def refresh_board(surface: pygame.surface.Surface, strands: StrandsGameBase, 
    pending: list[Pos], art: ArtGUIBase) -> None:
    """
    Draws the current state of the Board
    """
    #Uses the imported art to dra the frame
    art.draw_background(surface)
    FRAME = art.frame_width + 15
    
    board: BoardBase = strands.board()

    rows: int = board.num_rows()
    cols: int = board.num_cols()
    surface_width: int = CELL_SIZE * cols + (2 *FRAME)
    surface_height: int = CELL_SIZE * (rows + 1) + (2 * FRAME)
    font: pygame.font.Font = pygame.font.SysFont(None, 36)
    if not isinstance(art, ArtGUICat4):
        interior_rect = pygame.Rect(
            FRAME,
            FRAME,
            CELL_SIZE * cols,
            CELL_SIZE * rows
        )
        pygame.draw.rect(surface, COLORS["WHITE"], interior_rect)

    # Creates a set of positions for the found words and adds the lines between
    # the positions
    highlighted_positions: set[tuple[int, int]] = set()
    for word in strands.found_strands():
        positions: list[PosBase] = word.positions()
        if len(positions) >= 2:
            for i in range(len(positions) - 1):
                pos_1: PosBase = positions[i]
                pos_2: PosBase = positions[i + 1]
                x1: int = FRAME + pos_1.c * CELL_SIZE + CELL_SIZE // 2
                y1: int = FRAME + pos_1.r * CELL_SIZE + CELL_SIZE // 2
                x2: int = FRAME + pos_2.c * CELL_SIZE + CELL_SIZE // 2
                y2: int = FRAME + pos_2.r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(surface, COLORS["LIGHTBLUE"], (x1, y1), 
                    (x2, y2), width=4)
        for pos in positions:
            highlighted_positions.add((pos.r, pos.c))

    # Displays the pending selection with the color green
    for pos in pending:
        center: tuple[int, int] = (FRAME + pos.c * CELL_SIZE + CELL_SIZE // 2, 
            FRAME + pos.r * CELL_SIZE + CELL_SIZE // 2)
        radius: int = CELL_SIZE // 3
        pygame.draw.circle(surface, COLORS["GREEN"], center, radius)

    if len(pending) >= 2:    
        for i in range(len(pending) - 1):
            pending_pos_1: PosBase = pending[i]
            pending_pos_2: PosBase = pending[i + 1]
            x1 = FRAME + pending_pos_1.c * CELL_SIZE + CELL_SIZE // 2
            y1 = FRAME + pending_pos_1.r * CELL_SIZE + CELL_SIZE // 2
            x2 = FRAME + pending_pos_2.c * CELL_SIZE + CELL_SIZE // 2
            y2 = FRAME + pending_pos_2.r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(surface, COLORS["GREEN"], (x1, y1), 
                (x2, y2), width=4)

    # Draws the hints on the board only if the hint meter allows
    active_hint: tuple[int, bool] | None = strands.active_hint()
    if active_hint is not None:
        index: int
        ends: bool
        index, ends = active_hint
        hint_strand: StrandBase
        _, hint_strand = strands.answers()[index]
        hint_positions: list[PosBase] = hint_strand.positions()

        for i, pos in enumerate(hint_positions):
            center = (FRAME + pos.c * CELL_SIZE + CELL_SIZE // 2, FRAME + pos.r * CELL_SIZE + 
                CELL_SIZE // 2)
            radius = CELL_SIZE // 4
            if ends and (i == 0 or i == len(hint_positions) - 1):
                pygame.draw.circle(surface, COLORS["PINK"], center, radius)
            else:
                pygame.draw.circle(surface, COLORS["YELLOW"], center, radius)


    # Adds/Updates the letters on the surface as well as blue circles for words
    # that are already found
    for row in range(rows):
        for col in range(cols):
            position: PosBase = Pos(row, col)
            letter: str = board.get_letter(position)

            if (row, col) in highlighted_positions:
                center = (FRAME + col * CELL_SIZE + CELL_SIZE // 2, 
                    FRAME + row * CELL_SIZE + CELL_SIZE // 2)
                radius = CELL_SIZE // 3
                pygame.draw.circle(surface, COLORS["LIGHTBLUE"], center, radius)

            letter_surface: pygame.Surface = font.render(letter, True, 
                COLORS["BLACK"])
            letter_rect: pygame.Rect = letter_surface.get_rect(center = (
                FRAME + col * CELL_SIZE + CELL_SIZE // 2, 
                FRAME + row * CELL_SIZE + CELL_SIZE // 2)
                )
            surface.blit(letter_surface, letter_rect)

    # Adds/Updates the "found" phrase on the bottom
    hint_surface: pygame.Surface = font.render(f"Found {len(
        strands.found_strands())}/{len(strands.answers())} Use Hint", True, 
        COLORS["BLACK"])
    hint_rect: pygame.Rect = hint_surface.get_rect(center = (
        surface_width //2, 
        surface_height - (0.5 * CELL_SIZE) - FRAME)
        )
    pygame.draw.rect(surface, COLORS["WHITE"], hint_rect.inflate(20, 10))
    surface.blit(hint_surface, hint_rect)


def run_game(filename: str, show: bool = False, hint_threshold: int = 3, art: ArtGUIBase | None = None) -> None:
    """
    Plays a game of Strands on a pygame window
    """
    pygame.init()
    pygame.display.set_caption("Strands")
    currently_selected: list[Pos] = []

    game: StrandsGameBase = StrandsGame(filename, hint_threshold = hint_threshold)
    if show:
        strand: StrandBase
        for _, strand in game.answers():
            game.submit_strand(strand)
    board: BoardBase = game.board()
    rows: int = board.num_rows()
    cols: int = board.num_cols()
    FRAME = art.frame_width + 15
    surface_width: int = CELL_SIZE * cols + (2 * FRAME)
    surface_height: int = CELL_SIZE * (rows + 1) + (2 * FRAME)
    surface: pygame.Surface = pygame.display.set_mode((surface_width, 
        surface_height))
    clock: pygame.time.Clock = pygame.time.Clock()
    answers: list[tuple[str, StrandBase]] = game.answers()
    return_key_index: int = 0

    mouse_down = False
    running = True
    while running:
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_q:
                    running = False
                
                if not show:

                    if event.key == pygame.K_RETURN:
                        game.submit_strand(answers[return_key_index][1])
                        return_key_index += 1

                    if event.key == pygame.K_ESCAPE:
                        currently_selected.clear()

                    if event.key == pygame.K_h:
                        if game.hint_meter() >= game.hint_threshold():
                            game.use_hint()
                        else:
                            print("Hint meter too low.")

            elif event.type == pygame.MOUSEBUTTONDOWN and not show:
                x: int
                y: int
                x, y = event.pos
                col: int = (x - FRAME) // CELL_SIZE
                row: int = (y - FRAME) // CELL_SIZE
                cell_pos = Pos(row, col)

                if 0 <= row < rows and 0 <= col < cols:
                    currently_selected.clear()
                    currently_selected.append(cell_pos)
                    mouse_down = True

            elif event.type == pygame.MOUSEBUTTONUP and not show:
                    mouse_down = False

                    if len(currently_selected) >= 2:
                        start: Pos = currently_selected[0]
                        steps: list[Step] = [
                            currently_selected[i].step_to(
                            currently_selected[i + 1]) for i in 
                            range(len(currently_selected) - 1)]
                        strand = Strand(start, steps)

                        answer: StrandBase
                        for answer, answer_pos in answers:
                            if board.evaluate_strand(strand) == answer:
                                game.submit_strand(answer_pos)
                                currently_selected.clear()
                                break
                    currently_selected.clear()

            elif event.type == pygame.MOUSEMOTION and mouse_down and not show:    
                x: int
                y: int        
                x, y = event.pos
                col = (x - FRAME) // CELL_SIZE
                row = (y - FRAME) // CELL_SIZE
                cell_pos = Pos(row, col)

                if 0 <= row < rows and 0 <= col < cols:
                    center_x = FRAME + col * CELL_SIZE + CELL_SIZE // 2
                    center_y = FRAME + row * CELL_SIZE + CELL_SIZE // 2
                    dist = math.hypot(x - center_x, y - center_y)
                    
                    if dist < CELL_SIZE * 0.4:
                        if not currently_selected:
                            currently_selected.append(cell_pos)
                        else:
                            last_pos = currently_selected[-1]
                            if cell_pos != last_pos and cell_pos.is_adjacent_to(last_pos):
                                if cell_pos not in currently_selected:
                                    currently_selected.append(cell_pos)
                                else:
                                    index = currently_selected.index(cell_pos)
                                    currently_selected = currently_selected[:index + 1]

        refresh_board(surface, game, currently_selected, art)
        pygame.display.update()

        if not show and game.game_over():
            running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()


#Click Command-Line Commands

@click.command()
@click.option('--show', is_flag=True, help="Show the answers instead of playing the game.")
@click.option('-g', '--game', default=None, help="Game to load (ex: cs-142). Random if not provided.")
@click.option('-h', '--hint', default=3, type=int, help="Hint threshold (default: 3).")
@click.option('-a', '--art', default="stub", help="Art frame to use (ex: stub, cat1).")

def main(show: bool, game: str | None, hint: int, art: str):
    if game:
        filename = f"boards/{game}.txt"
    else:
        txt_files = [f for f in os.listdir("boards") if f.endswith(".txt")]
        if not txt_files:
            print("Can't find game file")
            sys.exit(1)
        filename = f"boards/{random.choice(txt_files)}"
    
    if art == "stub":
        art_frame = ArtGUIStub(frame_width=15)
    elif art == "9slices":
        art_frame = ArtGUI9Slice(frame_width=15)
    elif art == "cat3":
        art_frame = ArtGUICat3(frame_width=15)
    elif art == "cat4":
        art_frame = ArtGUICat4(frame_width=20)
    else:
        print(f"Art frame '{art}' not supported in GUI.")
        sys.exit(1)


    run_game(filename, show=show, hint_threshold=hint, art = art_frame)


if __name__ == "__main__":
    main()
