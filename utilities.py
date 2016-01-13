import pygame
import random
import math
import colors

logging_on = True


def log(*args, **kwargs):
    if logging_on:
        print(*args, **kwargs)


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def spawn_org():
    coords = []
    coords.append(random.randrange(21, 779))
    coords.append(random.randrange(21, 579))

    return coords


def gen_goblin_genes():
    genome = []
    genome.append(random.randrange(2, 3))
    return 2


def gen_ogre_genes():
    genome = []
    genome.append(random.randrange(3, 5))
    return 3


def get_vector(self, a, b, x, y):

    dist_x = abs(a - x)
    dist_y = abs(b - y)

    if dist_x > dist_y:
        if a > x:
            self.change_x = self.speed
        elif a < x:
            self.change_x = -self.speed
        else:
            self.change_y = 0

    elif dist_x < dist_y:
        if b > y:
            self.change_y = self.speed
        elif b < y:
            self.change_y = -self.speed
        else:
            self.change_x = 0
    else:
        if a > x:
            self.change_x = round(self.speed / 2)
        elif a < x:
            self.change_x = -round(self.speed / 2)
        else:
            self.change_x = 0
        if b > y:
            self.change_y = round(self.speed / 2)
        elif b < y:
            self.change_y = -round(self.speed / 2)
        else:
            self.change_y = 0
