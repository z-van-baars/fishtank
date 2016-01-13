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


def get_vector_old(self, a, b, x, y):

    dist_x = abs(a - x)
    dist_y = abs(b - y)

    top = (0, -self.speed)
    bottom = (0, self.speed)
    right = (self.speed, 0)
    left = (-self.speed, 0)
    top_left = ((self.speed * -0.25), (self.speed * -0.75))
    top_right = ((self.speed * 0.25), (self.speed * -0.75))
    right_top = ((self.speed * 0.75), (self.speed * -0.25))
    right_bottom = ((self.speed * 0.75), (self.speed * 0.25))
    bottom_left = ((self.speed * -0.25), (self.speed * 0.75))
    bottom_right = ((self.speed * 0.25), (self.speed * 0.75))
    left_top = ((self.speed * -0.75), (self.speed * -0.25))
    left_bottom = ((self.speed * -0.75), (self.speed * 0.25))

    if a > x:
        if dist_x > dist_y:
            if b == y:
                return right
            elif b < y:
                return right_top
            elif b > y:
                return right_bottom
        elif dist_x < dist_y:
            if b < y:
                return top_right
            elif b > y:
                return bottom_right
        elif dist_x == dist_y:
            if b > y:
                return ((self.speed * 0.5), (self.speed * 0.5))
            if b < y:
                return ((self.speed * 0.5), (self.speed * -0.5))
    elif a < x:
        if dist_x > dist_y:
            if b == y:
                return left
            elif b < y:
                return left_top
            elif b > y:
                return left_bottom
        elif dist_x < dist_y:
            if b < y:
                return top_left
            elif b > y:
                return bottom_left
        elif dist_x == dist_y:
            if b > y:
                return ((self.speed * -0.5), (self.speed * -0.5))
            if b < y:
                return ((self.speed * -0.5), (self.speed * 0.5))

    else:
        if b < y:
            return top
        elif b > y:
            return bottom
        else:
            return (0, 0)
