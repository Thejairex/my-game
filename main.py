import pygame
import socket
import pickle
import threading
from server import Server

class Juego:
    def __init__(self):
        pygame.init()
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Juego")
        self.clock = pygame.time.Clock()
        self.inGame = False

        self.fps = 60
        self.countPlayer = 0

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (0,0,255)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.colorPlayer = [self.white, self.blue, self.red, self.green]

        self.player_width = 50
        self.player_height = 50

        self.player1_init = False
        self.player2_init = False
        self.player1_x = 10
        self.player1_y = 10
        self.player2_x = self.size[0] - 10
        self.player2_y = 10        

        self.player_speed = 5

    def createPlayer(self):
        if self.player1_init:
                pygame.draw.rect(
                    self.screen, self.colorPlayer[self.countPlayer],
                    [self.player1_x, self.player1_y, self.player_width, self.player_height]
                )
                
        if self.player2_init:
            pygame.draw.rect(
                self.screen, self.colorPlayer[self.countPlayer+1],
                [self.player2_x, self.player2_y, self.player_width, self.player_height]
            )

    def host(self):
        self.server = Server("localhost", 5555)
        threading.Thread(target=self.server.run).start()

    def connectHost(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 5555))
        threading.Thread(target=self.recvPos).start()

    def recvPos(self):
        while True:
            dataServer = self.client.recv(4096)
            pos = pickle.loads(dataServer)
            self.player1_x = pos[0]
            self.player1_y = pos[1]

    def sendPos(self):
        try:
            player_position = (self.player1_x, self.player1_y)
            data = pickle.dumps((player_position))
            self.client.send(data)

        except Exception as e:
            if str(e) == "'Juego' object has no attribute 'client'":
                pass
            else:
                print(str(e))

    def controlSpace(self, player_x, player_y):
        if self.player1_x < 0:
            self.player1_x = 0
        elif self.player1_x > self.size[0] - self.player_width:
            self.player1_x = self.size[0] - self.player_width
        if self.player1_y < 0:
            self.player1_y = 0
        elif self.player1_y > self.size[1] - self.player_height:
            self.player1_y = self.size[1] - self.player_height
        pass

    def run(self):
        while not self.inGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.inGame = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player1_init = True

                    if event.key == pygame.K_2:
                        self.player2_init = True

                    if event.key == pygame.K_i:
                        self.host()

                    if event.key == pygame.K_u:
                        self.connectHost()

                    if event.key == pygame.K_v:
                        print(self.server.countClient())
                            
            keys = pygame.key.get_pressed()

            # Movimiento del Jugador 1
            if keys[pygame.K_LEFT]:
                self.player1_x -= self.player_speed
                self.sendPos()

            if keys[pygame.K_RIGHT]:
                self.player1_x += self.player_speed
                self.sendPos()

            if keys[pygame.K_UP]:
                self.player1_y -= self.player_speed
                self.sendPos()

            if keys[pygame.K_DOWN]:
                self.player1_y += self.player_speed
                self.sendPos()

            # # Movimiento del Jugador 2
            # if keys[pygame.K_a]:
            #     self.player2_x -= self.player_speed
            # if keys[pygame.K_d]:
            #     self.player2_x += self.player_speed
            # if keys[pygame.K_w]:
            #     self.player2_y -= self.player_speed
            # if keys[pygame.K_s]:
            #     self.player2_y += self.player_speed


            # Control de juego
            if keys[pygame.K_q]:
                self.inGame = True

            # Control de espacio del jugador 1
            self.controlSpace(self.player1_x, self.player1_y)

            # # Control de escpacio del jugador 2
            # if self.player2_x < 0:
            #     self.player2_x = 0
            # elif self.player2_x > self.size[0] - self.player_width:
            #     self.player2_x = self.size[0] - self.player_width
            # if self.player2_y < 0:
            #     self.player2_y = 0
            # elif self.player2_y > self.size[1] - self.player_height:
            #     self.player2_y = self.size[1] - self.player_height

            # Control de pantalla
            self.screen.fill(self.black)

            self.createPlayer()

            pygame.display.flip()
            self.clock.tick(self.fps)

    pygame.quit()

if __name__ == "__main__":
    game = Juego()
    game.run()