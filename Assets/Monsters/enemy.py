from Assets.entity import Entity

class Enemigo(Entity):
    def __init__(self, name=str) -> None:
        super().__init__()
        
        # Config
        self.name = name
        self.speed = 2
        
