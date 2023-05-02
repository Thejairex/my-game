import pygame
import pyganim

class Entity(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
    
    # method to animate Sheets
    def animateSheets(self,sheet, dim=int) -> pyganim.PygAnimation:
        frames = []
        for i in range(4):
            frame_x = i * dim
            frame_y = 0
            frame = sheet.subsurface((frame_x, frame_y, dim, dim))
            frames.append((frame, 175))
        return pyganim.PygAnimation(frames)