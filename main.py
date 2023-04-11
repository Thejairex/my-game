import pygame
import random

class Personaje:
    def __init__(self):
        self.speed = 5
        self.rect = pygame.Rect(10, 10, 50, 50)
        
    def draw(self, screen, color):
        return pygame.draw.rect(screen, color, self.rect)
    
class Arma:
    def __init__(self):
        self.name = "Gun"
        self.damage = 5
        self.alive = False
        self.posX = random.randint(10,700-10)
        self.posy = random.randint(10,500-10)

    def draw(self, screen, color):
        if not self.alive:
            self.posX = random.randint(10,700-10)
            self.posy = random.randint(10,500-10)
            self.alive = True
        self.rect = pygame.Rect(self.posX,self.posy,20,20)
        return pygame.draw.rect(screen, color, self.rect)
class Juego:
    def __init__(self):
        pygame.init()
        # Screen
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Juego")

        # Ticks
        self.timeTemp = 0
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255,0,0)

        # Events
        self.inGame = False

        # Settings
        self.mainFont = pygame.font.SysFont("Victor mono", 24)
        

        # Entities
        self.player = Personaje()
        self.weapon = Arma()

    def gameSpace(self):
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        elif self.player.rect.right > self.size[0]:
            self.player.rect.right = self.size[0]
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        elif self.player.rect.bottom > self.size[1]:
            self.player.rect.bottom = self.size[1]

    def run(self):
        while not self.inGame:
            # Time Game
            time = pygame.time.get_ticks()//1000 
            if self.timeTemp == time:
                self.timeTemp += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.inGame = True

            # Movimiento del Jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.rect.left -= self.player.speed
            if keys[pygame.K_RIGHT]:
                self.player.rect.right += self.player.speed
            if keys[pygame.K_UP]:
                self.player.rect.top -= self.player.speed
            if keys[pygame.K_DOWN]:
                self.player.rect.bottom += self.player.speed

            # Control de juego
            if keys[pygame.K_q]:
                self.inGame = True

            # Control de espacio del jugador
            self.gameSpace()
            
            # Control de pantalla
            pygame.display.flip()
            self.screen.fill(self.black)
            
            # Draw
            self.weapon.draw(self.screen, self.red)
            self.player.draw(self.screen, self.white)

            labelTime = self.mainFont.render(f"Tiempo: {time}",0, self.white)
            self.screen.blit(labelTime,
                            (self.size[0]//2 - labelTime.get_width()//2, 0))
            
            # Fps
            self.clock.tick(self.fps)

    pygame.quit()

if __name__ == "__main__":
    game = Juego()
    game.run()