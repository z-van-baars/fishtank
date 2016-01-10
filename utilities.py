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


def place_in_chunk(me, current_room):

    for row in range(len(current_room.chunk_rows)):
        for column in range(len(current_room.chunk_rows[row])):
            this_chunk = current_room.chunk_rows[row][column]
            if this_chunk.left <= me.rect.x and me.rect.x <= this_chunk.right:
                if this_chunk.top <= me.rect.y and me.rect.y <= this_chunk.bottom:
                    if me.species == "Coin":
                        this_chunk.coins_list.add(me)
                        me.current_chunk_row = row
                        me.current_chunk_column = column
                        me.current_chunk = this_chunk
                    elif me.species == "Goblin":
                        this_chunk.goblins_list.add(me)
                        me.current_chunk_row = row
                        me.current_chunk_column = column
                        me.current_chunk = this_chunk
                    elif me.species == "Ogre":
                        this_chunk.ogres_list.add(me)
                        me.current_chunk_row = row
                        me.current_chunk_column = column
                        me.current_chunk = this_chunk

    me.neighbors = (get_valid_neighbors(me, me.current_chunk_row, me.current_chunk_column))


def get_valid_neighbors(me, current_chunk_row, current_chunk_column):
        chunks = me.current_room.chunk_rows
        neighbors = []

        if current_chunk_row > 0:
            neighbors.append(chunks[current_chunk_row - 1]
                                   [current_chunk_column])  # top center
            if current_chunk_column > 0:
                neighbors.append(chunks[current_chunk_row - 1]
                                       [current_chunk_column - 1])  # top left
            elif current_chunk_column < 6:
                neighbors.append(chunks[current_chunk_row - 1]
                                       [current_chunk_column + 1])  # top right

        if current_chunk_row < 6:
            neighbors.append(chunks[current_chunk_row + 1]
                                   [current_chunk_column])  # bottom center
            if current_chunk_column > 0:
                neighbors.append(chunks[current_chunk_row + 1]
                                       [current_chunk_column - 1])  # bottom left
            if current_chunk_column < 6:
                neighbors.append(chunks[current_chunk_row + 1]
                                       [current_chunk_column + 1])  # bottom right

        if current_chunk_column < 7:
            neighbors.append(chunks[current_chunk_row]
                                   [current_chunk_column + 1])  # right

        if current_chunk_column > 0:
            neighbors.append(chunks[current_chunk_row]
                                   [current_chunk_column - 1])  # left

        return neighbors


def remove_from_chunk(me, species, chunk):
    
    if species == "Coin":
        chunk.coins_list.remove(me)
    elif species == "Goblin":
        chunk.goblins_list.remove(me)
    elif species == "Ogre":
        chunk.ogres_list.remove(me)
    elif species == "Wall":
        chunk.walls_list.remove(me)
