# importacion de librerias
import pygame
import random

# Importacion de modulos
class ObjetoJuego:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        
    def draw(self, screen, color):
        return pygame.draw.rect(screen, color, self.rect)
class Personaje(ObjetoJuego):
    def __init__(self) -> None:
        super().__init__(50, 50)
        self.speed = 5
        self.rect.x = 10
        self.rect.y = 10

class Enemigo(ObjetoJuego):
    def __init__(self) -> None:
        super().__init__(15, 15)
        self.name = "Monster"
        self.speed = 2
        self.rect.x = random.randint(15, 685-self.width)
        self.rect.y = random.randint(15, 485-self.width)


class Arma(ObjetoJuego):
    def __init__(self):
        super().__init__(20, 20)
        self.name = "Gun"
        self.damage = 5
        self.alive = False

    def draw(self, screen, color):
        if not self.alive:
            self.posX = random.randint(10, 700-10)
            self.posY = random.randint(10, 500-10)
            self.alive = True
            
        self.rect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        return pygame.draw.rect(screen, color, self.rect)

    def destroy(self):
        self.width = 0
        self.height = 0
        self.posX = 0
        self.posY = 0


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
        self.weapon = Arma()
        self.listEnemies = [] 

    def gameSpace(self):
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        elif self.player.rect.right > self.size[0]:
            self.player.rect.right = self.size[0]
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        elif self.player.rect.bottom > self.size[1]:
            self.player.rect.bottom = self.size[1]

    # Generations
    def generateEntities(self):
        self.weapon.draw(self.screen, self.colorWeapon)
        self.player.draw(self.screen, self.white)
        while len(self.listEnemies) < self.maxEnemies:
            self.listEnemies.append(Enemigo())
        
        for enemy in self.listEnemies:
            enemy.draw(self.screen, self.blue)
    
    # Metodos logicos del juego
    def colliders(self):
        if self.player.rect.colliderect(self.weapon.rect):
            self.weapon.destroy()
            
        # Enemies
        to_remove = []
        for enemy in self.listEnemies:
            if enemy.rect.colliderect(self.player.rect):
                to_remove.append(enemy)
        
        self.listEnemies = [enemy for enemy in self.listEnemies if enemy not in to_remove]
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
            self.gameSpace()

            # Control de pantalla
            pygame.display.flip()
            self.screen.fill(self.black)

            # Draw Entities
            self.generateEntities()

            # Logica del juego.
            self.colliders()
            self.followPlayer()
            self.upMaxEnemies()

            labelTime = self.mainFont.render(timeConv, 0, self.white)
            labelEnemyKilled = self.mainFont.render(f"Enemigos eliminados: {self.totalEnemiesKilled}", 0, self.white)
            self.screen.blit(labelTime,
                             (self.size[0]//2 - labelTime.get_width()//2, 0))
            self.screen.blit(labelEnemyKilled,
                             (self.size[0]//2 - labelEnemyKilled.get_width()//2,labelTime.get_height()))

            # Fps
            self.clock.tick(self.fps)

    pygame.quit()


if __name__ == "__main__":
    game = Juego()
    game.run()
