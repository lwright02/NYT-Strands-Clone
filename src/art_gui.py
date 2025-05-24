import click
import sys
import pygame
import math
from ui import ArtGUIBase, GUIStub

class ArtGUI9Slice(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        fw = self.frame_width

        colors = {
            "tl": (255, 100, 7),
            "tr": (60, 180, 110),
            "bl": (70, 130, 180),
            "br": (255, 165, 0),
            "top": (125, 105, 235),
            "bottom": (0, 195, 255),
            "left": (255, 105, 180),
            "right": (145, 240, 145),
            "center": (210, 250, 255)
        }

        pygame.draw.rect(surface, colors["tl"], (0, 0, fw, fw))
        pygame.draw.rect(surface, colors["tr"], (w-fw, 0, fw, fw))
        pygame.draw.rect(surface, colors["bl"], (0, h-fw, fw, fw))
        pygame.draw.rect(surface, colors["br"], (w-fw, h-fw, fw, fw))

        pygame.draw.rect(surface, colors["top"], (fw, 0, w-2*fw, fw))
        pygame.draw.rect(surface, colors["bottom"], (fw, h-fw, w-2*fw, fw))
        pygame.draw.rect(surface, colors["left"], (0, fw, fw, h-2*fw))
        pygame.draw.rect(surface, colors["right"], (w-fw, fw, fw, h-2*fw))

        pygame.draw.rect(surface, colors["center"], (fw, fw, w-2*fw, h-2*fw))

class ArtGUICat3(ArtGUIBase):
    def __init__(self, frame_width: int):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        hex_radius = 20
        hex_height = hex_radius * 2
        hex_width = int(1.732 * hex_radius)
        vert_spacing = int(0.75 * hex_height)

        def hexagon_points(cx, cy):
            points = []
            for i in range(6):
                angle = i * 60 * 3.14159 / 180
                x = cx + hex_radius * math.cos(angle)
                y = cy + hex_radius * math.sin(angle)
                points.append((x, y))
            return points
        
        for y in range(0, h + hex_height, vert_spacing):
            for x in range(0, w + hex_width, hex_width):
                offset = hex_width // 2 if (y // vert_spacing) % 2 == 1 else 0
                points = hexagon_points(x + offset, y)
                pygame.draw.polygon(surface, (255, 215, 0), points, 1)

class ArtGUICat4(ArtGUIBase):
    def __init__(self, frame_width: int = 20):
        self.frame_width = frame_width

    def draw_background(self, surface: pygame.Surface) -> None:
        w, h = surface.get_width(), surface.get_height()
        surface.fill((245, 255, 250))
        center_x, center_y = w // 2, h // 2
        spacing = 60
        nodes = [
            (center_x - spacing, center_y - spacing),
            (center_x, center_y - spacing - 20),
            (center_x + spacing, center_y - spacing),
            (center_x - spacing // 2, center_y + spacing // 2),
            (center_x + spacing // 2, center_y + spacing // 2),
            (center_x, center_y + spacing + 20)
        ]
        for (x, y) in nodes:
            pygame.draw.circle(surface, (50, 100, 200), (x, y), 10)
        edges = [(0, 1), (1, 2), (0, 3), (1, 4), (3, 5), (4, 5)]
        for i, j in edges:
            pygame.draw.line(surface, (100, 100, 100), nodes[i], nodes[j], 2)

@click.command()
@click.option('-a', '--art', required=True, help="Art frame: 9slices, cat3, cat4.")
@click.option('-f', '--frame', type=int, help="Frame width in pixels.")
@click.option('-w', '--width', type=int, help="Window width in pixels.")
@click.option('-h', '--height', type=int, help="Window height in pixels.")
def main(art, frame, width, height):
    supported = {
        "9slices": ArtGUI9Slice,
        "cat0": ArtGUI9Slice,
        "cat3": ArtGUICat3,
        "cat4": ArtGUICat4
    }

    if art not in supported:
        click.echo(f"Pattern '{art}' is not supported in GUI.")
        return

    cls = supported[art]

    if art in {"cat4"}:
        gui = GUIStub(cls(), 300, 400)
        gui.run_event_loop()
    else:
        if frame is None or width is None or height is None:
            click.echo("Missing options: --frame, --width, and --height are required unless using cat4.")
            return
        gui = GUIStub(cls(frame), width, height)
        gui.run_event_loop()

if __name__ == "__main__":
    main()
