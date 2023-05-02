import pygame
import pyganim

from Assets.entity import Entity


class Personaje(Entity):
    def __init__(self) -> None:
        super().__init__()

        # Loading Sprites Player
        spriteTemp = pygame.transform.scale(
            pygame.image.load("Sprites/Player/Player.png"), (80, 80))
        spriteIdle = pygame.image.load("Sprites/Player/PlayerIdle.png")
        spriteMovements = pygame.image.load("Sprites/Player/PlayerMovents.png")

        # Rect
        self.rect = spriteTemp.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        # Config
        self.speed = 5
        self.moveState = False
        self.moveDirection = "right"

        # Animation Movements
        self.animMovements = self.animateSheets(spriteMovements, 16)
        self.animMovements.play()
        self.animMovements.scale((self.rect.width, self.rect.height))

        # Animation Idle
        self.animIdle = self.animateSheets(spriteIdle, 16)
        self.animIdle.play()
        self.animIdle.scale((self.rect.width, self.rect.height))

    def draw(self, screen):
        if self.moveState:
            return self.animMovements.blit(screen, self.rect)
        else:
            return self.animIdle.blit(screen, self.rect)

    def flipAnimation(self, direction):
        if self.moveDirection != direction:
            self.animMovements.flip(True, False)
            self.animIdle.flip(True, False)
            self.moveDirection = direction

    def gameSpace(self, size):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > size[0]:
            self.rect.right = size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > size[1]:
            self.rect.bottom = size[1]
