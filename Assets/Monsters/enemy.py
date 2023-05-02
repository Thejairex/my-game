from Assets.entity import Entity


class Enemigo(Entity):
    def __init__(self, name=str, width=int, height=int) -> None:
        super().__init__(width, height)

        # Config
        self.name = name
        self.speed = 2
