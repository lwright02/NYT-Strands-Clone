import sys
import pygame
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

if __name__ == "__main__":
    fw, width, height = map(int, sys.argv[1:])
    gui = GUIStub(ArtGUI9Slice(fw), width, height)
    gui.run_event_loop()