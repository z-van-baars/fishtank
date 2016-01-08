import pygame
import random
import math
import colors

logging_on = True


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


def log(*args, **kwargs):
    if logging_on:
        print(*args, **kwargs)
