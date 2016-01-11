import entity
import colors

class Coin(entity.Entity):
    def __init__(self, x, y, current_room):
        super().__init__(x, y, current_room, colors.gold, 5, 5)

    def __lt__(self, other):
        if self.rect.x < other.rect.x:
            return True
        elif self.rect.y < other.rect.y:
            return True
        else:
            return False
