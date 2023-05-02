import pygame

class Spyhole:
    def __init__(self) -> None:
        self.sprite = pygame.image.load("Sprites/Others/spyhole.png")
        self.rect = self.sprite.get_rect()
    
    def pos(self, mouse):
        self.rect.centerx = mouse[0]
        self.rect.centery = mouse[1]
    
    def draw(self, screen):
        return screen.blit(self.sprite, self.rect)