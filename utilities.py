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


def place_in_chunk(self, current_room):

    for chunk in current_room.chunk_dict:
        this_chunk = current_room.chunk_dict[chunk]
        if this_chunk.left <= self.rect.x < this_chunk.right and this_chunk.top <= self.rect.y < this_chunk.bottom:
            if self.species == "Coin":
                current_room.chunk_dict[chunk].coins_list.add(self)
                self.current_chunk = chunk
            elif self.species == "Goblin":
                current_room.chunk_dict[chunk].goblins_list.add(self)
                self.current_chunk = chunk
            elif self.species == "Ogre":
                current_room.chunk_dict[chunk].ogres_list.add(self)
                self.current_chunk = chunk
        else:
            print("something wasn't properly chunked!")


def remove_from_chunk(self):
    chunk = self.current_room.chunk_dict[self.current_chunk]
    species = self.species
    if species == "Coin":
        chunk.coins_list.remove(self)
    elif species == "Goblin":
        chunk.goblins_list.remove(self)
    elif self.species == "Ogre":
        chunk.ogres_list.remove(self)
