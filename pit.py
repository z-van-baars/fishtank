import pygame
import entity
import colors
import goblin

pygame.init()
pygame.display.set_caption("There's always a bigger fish")
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
pit_img = pygame.image.load("art/pit.png")
pit_img.set_colorkey(colors.key)


class Pit(entity.Entity):

    def __init__(self, x, y, current_room):
        super().__init__((x - 20), (y - 15), current_room, colors.white, 40, 30)
        self.image = pit_img
        self.lifetime_coins = 0
        self.coins = 0

    def spawn_goblin(self):
        new_goblin = goblin.Goblin(self.rect.x + 15, self.rect.y + 35, self.current_room)
        new_goblin.place_in_chunk(self.current_room)
        self.current_room.entity_list[type(new_goblin)].add(new_goblin)
        self.coins -= 15
