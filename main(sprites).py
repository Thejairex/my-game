# importacion de librerias
import pygame
import random
import pyganim


class Personaje(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.spritePlayer = pygame.image.load("Sprites/Player/PlayerIdle.png")
        self.speed = 5
        frames = []
        for i in range(4):
            frame_x = i * 16
            frame_y = 0
            frame = self.spritePlayer.subsurface((frame_x, frame_y, 16, 16))
            frames.append((frame, 100))

        print(len(frames))
        self.animation = pyganim.PygAnimation(frames)
        self.animation.play()
        self.animation.scale((50,50))
        self.rect = self.animation.getRect()
        
        
    def draw(self, screen):
        return self.animation.blit(screen, (100, 100))

    # def draw(self):
    #     return self.animation.play()

    def gameSpace(self, size):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > size[0]:
            self.rect.right = size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > size[1]:
            self.rect.bottom = size[1]


class Juego:
    def __init__(self):
        pygame.init()
        # Screen
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Juego")

        # Ticks
        self.secondsTemp = 0
        self.minutes = 0
        self.clock = pygame.time.Clock()
        self.fps = 120

        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.colorWeapon = self.red

        # Events
        self.inGame = False
        self.totalEnemiesKilled = 0
        self.enemiesKilled = 0

        # Settings
        self.mainFont = pygame.font.SysFont("Dancing Script", 24)
        self.maxEnemies = 3

        # Entities
        self.player = Personaje()
        # self.weapon = Arma()
        self.listEnemies = []

    # Generations
    def generateEntities(self):
        # self.weapon.draw(self.screen, self.colorWeapon)
        self.player.draw(self.screen)

        # while len(self.listEnemies) < self.maxEnemies:
        #     self.listEnemies.append(Enemigo())

        # for enemy in self.listEnemies:
        #     enemy.draw(self.screen, self.blue)
        #     enemy.notCollision([enemyTemp for enemyTemp in self.listEnemies if enemyTemp != enemy])

    # Metodos logicos del juego
    def colliders(self):
        if self.player.rect.colliderect(self.weapon.rect):
            self.weapon.destroy()

        # Enemies
        to_remove = []
        for enemy in self.listEnemies:
            if enemy.rect.colliderect(self.player.rect):
                to_remove.append(enemy)

        self.listEnemies = [
            enemy for enemy in self.listEnemies if enemy not in to_remove]
        self.totalEnemiesKilled += self.maxEnemies - len(self.listEnemies)
        self.enemiesKilled += self.maxEnemies - len(self.listEnemies)

    def followPlayer(self):
        for enemy in self.listEnemies:
            if enemy.rect.x < self.player.rect.centerx:
                enemy.rect.x += enemy.speed
            if enemy.rect.x > self.player.rect.centerx:
                enemy.rect.x -= enemy.speed
            if enemy.rect.y < self.player.rect.centery:
                enemy.rect.y += enemy.speed
            if enemy.rect.y > self.player.rect.centery:
                enemy.rect.y -= enemy.speed

    def upMaxEnemies(self):
        if self.enemiesKilled % 50 == 0 and self.enemiesKilled != 0:
            self.maxEnemies += 1
            self.enemiesKilled = 0

    def time_conversion(self):
        if self.secondsTemp >= 60:
            if self.secondsTemp % 60 == 0:
                self.minutes += 1
            secondsConv = self.secondsTemp - (60 * self.minutes)
            return f"Tiempo: {self.minutes}m {secondsConv}s"
        else:
            return f"Tiempo: {self.secondsTemp}s"

    def run(self):
        
        while not self.inGame:
            # Time Game
            self.seconds = pygame.time.get_ticks()//1000
            if self.secondsTemp == self.seconds:
                self.secondsTemp += 1
                timeConv = self.time_conversion()

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
            # self.player.gameSpace(self.size)

            # Control de pantalla
            pygame.display.flip()
            self.screen.fill(self.black)

            # Draw Entities
            self.generateEntities()
            
            self.player.rect.x += self.player.speed
            # # Logica del juego.
            # self.colliders()
            # self.followPlayer()
            # self.upMaxEnemies()

            # Texto del juego.
            labelTime = self.mainFont.render(timeConv, 0, self.white)
            labelEnemyKilled = self.mainFont.render(
                f"Enemigos eliminados: {self.totalEnemiesKilled}", 0, self.white)

            self.screen.blit(labelTime,
                             (self.size[0]//2 - labelTime.get_width()//2, 0))
            self.screen.blit(labelEnemyKilled,
                             (self.size[0]//2 - labelEnemyKilled.get_width()//2, labelTime.get_height()))

            # Fps
            self.clock.tick(self.fps)

    pygame.quit()


if __name__ == "__main__":
    game = Juego()
    game.run()
