import random
import pygame

class Puntos:
    def __init__(self):
        self.posX = random.randint(10, 700-15)
        self.posY = random.randint(10, 500-15)
        self.width = 5
        self.height = 5
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)

    def draw(self, screen, color):
        return pygame.draw.rect(screen, color, self.rect)