# Importacion de Librerias
import pygame

# Importacion de modulos
from Assets.Entities.entity import Entity


class Arrow(Entity):
    def __init__(self) -> None:
        super().__init__(width=10, height=10)

        self.sprite = pygame.image.load("Sprites/Others/arrow.png")
        self.speed = 10
        self.alive = False
        

    def draw(self, screen=pygame.Surface):
        return self.sprite(screen, self.rect)
