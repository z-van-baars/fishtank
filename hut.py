import pygame
import utilities
import entity
import random
import colors
import goblin
import ogre

pygame.init()
pygame.display.set_caption("There's always a bigger fish")
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
hut_img = pygame.image.load("art/hut2.png")
hut_img.set_colorkey(colors.key)


class Hut(entity.Entity):

    def __init__(self, x, y, current_room):
        super().__init__((x - 20), (y - 15), current_room, colors.white, 40, 30)
        self.image = hut_img
        self.entity_list = {}
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        self.entity_list[ogre.Ogre] = pygame.sprite.Group()

    def update(self):
        nearby_goblins = pygame.sprite.Group()
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        # print(self.entity_list[goblin.Goblin])
        for each in self.neighbors:
            # print(each)
            # print(each.left, each.top)
            nearby_goblins.add(each.entity_list[goblin.Goblin])
            self.entity_list[goblin.Goblin].add(nearby_goblins)
        # print(self.entity_list[goblin.Goblin])
