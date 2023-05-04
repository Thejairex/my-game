# Importacion de Librerias
import pygame
import math

# Importacion de modulos
from Assets.Entities.entity import Entity


class Arrow(Entity):
    def __init__(self, width=40, height=10, target_pos=tuple, init_pos=tuple) -> None:
        super().__init__(width=width, height=height)

        self.target_pos = target_pos

        # Sprite
        self.sprite = pygame.transform.scale(
            pygame.image.load("Sprites/Others/arrow.png"), (width, height))

        # Config
        self.speed = 7
        self.rect.center = init_pos

        # Rotate image
        self.delta_X = self.target_pos[0] - self.rect.x
        self.delta_Y = self.target_pos[1] - self.rect.y
        angle = math.atan2(self.delta_Y, self.delta_X) * 180 / math.pi
        self.sprite = pygame.transform.rotate(self.sprite, -angle)
        self.rect = self.sprite.get_rect(center=self.rect.center)

    def draw(self, screen) -> pygame.Surface.blit:
        return screen.blit(self.sprite, self.rect)

    def moveToObjetive(self):
        dist = math.sqrt(self.delta_X**2 + self.delta_Y**2)
        if dist > 0:
            dx_norm = self.delta_X / dist
            dy_norm = self.delta_Y / dist
            dx_move = dx_norm * self.speed
            dy_move = dy_norm * self.speed

            if dist > self.speed:
                self.rect.move_ip(dx_move, dy_move)
            else:
                self.rect.center = self.target_pos
