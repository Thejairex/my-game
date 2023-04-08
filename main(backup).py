import pygame

class Juego:
    def __init__(self):
        pygame.init()
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Juego")
        self.clock = pygame.time.Clock()
        self.inGame = False

        self.fps = 60
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        
        self.player_width = 50
        self.player_height = 50
        self.player_init_x = 10
        self.player_init_y = 10

        self.player_speed = 5
        

    def run(self):
        while not self.inGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.inGame = True

            # Movimiento del Jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player_init_x -= self.player_speed
            if keys[pygame.K_RIGHT]:
                self.player_init_x += self.player_speed
            if keys[pygame.K_UP]:
                self.player_init_y -= self.player_speed
            if keys[pygame.K_DOWN]:
                self.player_init_y += self.player_speed

            # Control de juego
            if keys[pygame.K_q]:
                self.inGame = True

            # Control de espacio del jugador
            if self.player_init_x < 0:
                self.player_init_x = 0
            elif self.player_init_x > self.size[0] - self.player_width:
                self.player_init_x = self.size[0] - self.player_width
            if self.player_init_y < 0:
                self.player_init_y = 0
            elif self.player_init_y > self.size[1] - self.player_height:
                self.player_init_y = self.size[1] - self.player_height

            # Control de pantalla
            self.screen.fill(self.black)
            pygame.draw.rect(
                self.screen, self.white,
                [self.player_init_x, self.player_init_y, self.player_width, self.player_height])

            pygame.display.flip()
            self.clock.tick(self.fps)

    pygame.quit()

if __name__ == "__main__":
    game = Juego()
    game.run()