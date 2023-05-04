# importacion de librerias
import pygame


# Importacion de modulos
from Assets.Entities.player import Personaje
from Assets.Entities.Monsters.slime import Slime
from Assets.spyhole import Spyhole

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
        self.timeConv = self.secondsTemp

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
        self.spyhole = Spyhole()
        pygame.mouse.set_visible(False)

        # Entities
        self.player = Personaje(self.size)
        self.listEnemies = []

    # Generations
    def generateEntities(self):
        # Player
        self.player.draw(self.screen)
        
        # Mouse Spyhole
        self.spyhole.pos(pygame.mouse.get_pos())
        self.spyhole.draw(self.screen)

        # Enemies
        while len(self.listEnemies) < self.maxEnemies:
            self.listEnemies.append(Slime())

        for enemy in self.listEnemies:
            enemy.draw(self.screen)
        #     enemy.notCollision([enemyTemp for enemyTemp in self.listEnemies if enemyTemp != enemy])

    # Metodos logicos del juego
    def colliders(self):

        # Elimited Enemies
        # to_remove = []
        # for enemy in self.listEnemies:
        #     if enemy.rect.colliderect(self.player.rect):
        #         to_remove.append(enemy)

        # self.listEnemies = [
        #     enemy for enemy in self.listEnemies if enemy not in to_remove]

        # # Score Control
        # self.totalEnemiesKilled += self.maxEnemies - len(self.listEnemies)
        # self.enemiesKilled += self.maxEnemies - len(self.listEnemies)
        
        for enemy in self.listEnemies:
            if enemy.rect.colliderect(self.player.rect):
                self.inGame = True

    def killEnemy(self):
        to_remove = []
        for enemy in self.listEnemies:
            if enemy.rect.colliderect(self.spyhole.rect):
                to_remove.append(enemy)

        self.listEnemies = [
            enemy for enemy in self.listEnemies if enemy not in to_remove]

        # Score Control
        self.totalEnemiesKilled += self.maxEnemies - len(self.listEnemies)
        self.enemiesKilled += self.maxEnemies - len(self.listEnemies)

    def followPlayer(self):
        for enemy in self.listEnemies:
            if enemy.rect.centerx < self.player.rect.centerx:
                enemy.rect.centerx += enemy.speed
            if enemy.rect.centerx > self.player.rect.centerx:
                enemy.rect.centerx -= enemy.speed
            if enemy.rect.centery < self.player.rect.centery:
                enemy.rect.centery += enemy.speed
            if enemy.rect.centery > self.player.rect.centery:
                enemy.rect.centery -= enemy.speed

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
                self.timeConv = self.time_conversion()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.inGame = True
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("click izquierdo en: ", pygame.mouse.get_pos())
                        self.killEnemy()

            # Movimiento del Jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.rect.left -= self.player.speed
                self.player.moveState = True
                self.player.flipAnimation('left')

            if keys[pygame.K_d]:
                self.player.rect.right += self.player.speed
                self.player.moveState = True
                self.player.flipAnimation('right')

            if keys[pygame.K_w]:
                self.player.rect.top -= self.player.speed
                self.player.moveState = True

            if keys[pygame.K_s]:
                self.player.rect.bottom += self.player.speed
                self.player.moveState = True

            if not (keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]):
                self.player.moveState = False
            # Control de juego
            if keys[pygame.K_q]:
                self.inGame = True

            # Control de espacio del jugador
            self.player.gameSpace(self.size)

            # Control de pantalla
            pygame.display.flip()
            self.screen.fill(self.black)

            # Draw Entities
            self.generateEntities()

            # self.player.rect.x += self.player.speed
            # # Logica del juego.
            self.colliders()
            self.followPlayer()
            self.upMaxEnemies()

            # Texto del juego.
            labelTime = self.mainFont.render(self.timeConv, 1, self.white)
            labelEnemyKilled = self.mainFont.render(
                f"Enemigos eliminados: {self.totalEnemiesKilled}", 1, self.white)

            self.screen.blit(labelTime,
                             (self.size[0]//2 - labelTime.get_width()//2, 0))
            self.screen.blit(labelEnemyKilled,
                             (self.size[0]//2 - labelEnemyKilled.get_width()//2, labelTime.get_height()))

            # Fps
            self.clock.tick(self.fps)

        self.gameOver()

    def gameOver(self):
        print("Game Over")

    pygame.quit()


if __name__ == "__main__":
    game = Juego()
    game.run()
