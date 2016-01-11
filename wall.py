import entity

class Wall(entity.Entity):

    def __init__(self, x, y, current_room, color, width, height):
        super().__init__(x, y, current_room, color, width, height)
