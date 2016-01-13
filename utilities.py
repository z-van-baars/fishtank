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
    distance_to_target = distance(a, b, x, y)
    factor = distance_to_target / self.speed
    x_dist = a - x
    y_dist = b - y
    change_x = x_dist / factor
    change_y = y_dist / factor
    change_x = round(change_x)
    change_y = round(change_y)

    return (change_x, change_y)
