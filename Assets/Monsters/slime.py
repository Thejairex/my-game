# Importacion de Librerias
import pygame
import random

# Importacion de modulos
from Assets.Monsters.enemy import Enemigo


class Slime(Enemigo):
    def __init__(self) -> None:
        super().__init__(name="Slime", width=25, height=25)

        # Load Sprite Slime
        spriteIdle = pygame.image.load("Sprites/Enemies/Slimes/slimeIdle.png")

        # Rect
        self.rect.x = random.randint(self.rect.width+15, 685-self.rect.width)
        self.rect.y = random.randint(self.rect.height+15, 485-self.rect.width)

        # Animation Idle
        self.animIdle = self.animateSheets(spriteIdle, 24)
        self.animIdle.play()
        self.animIdle.scale((self.rect.width, self.rect.height))

    def draw(self, screen):
        return self.animIdle.blit(screen, self.rect)
