import pygame
import utilities
import entity
import random
import colors

pygame.init()
pygame.display.set_caption("There's always a bigger fish")
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
hut_img = pygame.image.load("art/hut.png")
hut_img.set_colorkey(colors.key)


class Hut(entity.Entity):

    def __init__(self, x, y, current_room):
        super().__init__((x - 20), (y - 15), current_room, colors.white, 40, 30)
        self.image = hut_img
