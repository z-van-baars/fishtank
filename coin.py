import entity
import colors
import pygame
import wall
import hut


class Coin(entity.Entity):
    def __init__(self, x, y, current_room):
        super().__init__(x, y, current_room, colors.gold, 5, 5)

        def collide(self):
            wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
            hut_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[hut.Hut], False)
            hit_lists = (wall_hit_list, hut_hit_list)
            for hit_list in hit_lists:
                for item in hit_list:
                    self.rect.x = (item.rect.right + 1)
                    self.rect.y = (item.rect.bottom + 1)
        collide(self)
