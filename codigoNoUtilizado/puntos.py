from Entities.puntos import Puntos


class Juego:
    def __init__(self):
        
    # Settings
        self.mainFont = pygame.font.SysFont("Dancing Script", 24)
        self.maxPoints = 5
        self.listPoints = []


    def points(self):
        while len(self.listPoints) < self.maxPoints:
            self.listPoints.append(Puntos())

        to_remove = []
        for point in self.listPoints:
            if self.player.rect.colliderect(point.rect):
                print("toque un punto")
                to_remove.append(point)
        self.listPoints = [
            point for point in self.listPoints if point not in to_remove]

    def run(self):
        for point in self.listPoints:
                    point.draw(self.screen, self.yellow)
                    
        self.points()