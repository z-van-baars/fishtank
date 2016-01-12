import entity
import colors

class Coin(entity.Entity):
    def __init__(self, x, y, current_room):
        super().__init__(x, y, current_room, colors.gold, 5, 5)