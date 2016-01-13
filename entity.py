import pygame
import colors
import utilities

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, current_room, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_chunk = None
        self.current_chunk_row = None
        self.current_chunk_column = None
        self.current_room = current_room
        self.neighbors = None

    def __lt__(self, other):
        if self.rect.x < other.rect.x:
            return True
        elif self.rect.y < other.rect.y:
            return True
        else:
            return False

    def expire(self):
        self.current_room.entity_list[type(self)].remove(self)
        self.current_chunk.entity_list[type(self)].remove(self)

    def place_in_chunk(self, current_room):
        for row in range(len(current_room.chunks)):
            for column in range(len(current_room.chunks[row])):
                this_chunk = current_room.chunks[row][column]
                if this_chunk.left <= self.rect.x <= this_chunk.right and this_chunk.top <= self.rect.y <= this_chunk.bottom:
                    this_chunk.entity_list[type(self)].add(self)
                    self.current_chunk_row = row
                    self.current_chunk_column = column
                    self.current_chunk = this_chunk
        assert self.current_chunk

        self.neighbors = (self.get_valid_neighbors(self.current_chunk_row, self.current_chunk_column))


    def get_valid_neighbors(self, current_chunk_row, current_chunk_column):
        chunks = self.current_room.chunks
        neighbors = []

        valid_chunks = [
            [True, True, True],
            [True, True, True],
            [True, True, True],
            ]


        # if you're in the top row of chunks
        if current_chunk_row == 0:
            valid_chunks[0][0] = False
            valid_chunks[0][1] = False
            valid_chunks[0][2] = False

        # if you're in the first column
        if current_chunk_column == 0:
            valid_chunks[0][0] = False
            valid_chunks[1][0] = False
            valid_chunks[2][0] = False

        # if you're in the last column
        if current_chunk_column == (len(chunks[0]) -1):
            valid_chunks[0][2] = False
            valid_chunks[1][2] = False
            valid_chunks[2][2] = False

        # if you're in the bottom column
        if current_chunk_row == (len(chunks) - 1):
            valid_chunks[2][0] = False
            valid_chunks[2][1] = False
            valid_chunks[2][2] = False

        if valid_chunks[0][0]:
            neighbors.append((chunks[current_chunk_row - 1][current_chunk_column - 1]))
        if valid_chunks[0][1]:
            neighbors.append((chunks[current_chunk_row - 1][current_chunk_column]))
        if valid_chunks[0][2]:
            neighbors.append((chunks[current_chunk_row - 1][current_chunk_column + 1]))
        if valid_chunks[1][0]:
            neighbors.append((chunks[current_chunk_row][current_chunk_column - 1]))
        if valid_chunks[1][1]:
            neighbors.append((chunks[current_chunk_row][current_chunk_column]))
        if valid_chunks[1][2]:
            neighbors.append((chunks[current_chunk_row][current_chunk_column + 1]))
        if valid_chunks[2][0]:
            neighbors.append((chunks[current_chunk_row + 1][current_chunk_column - 1]))
        if valid_chunks[2][1]:
            neighbors.append((chunks[current_chunk_row + 1][current_chunk_column]))
        if valid_chunks[2][2]:
            neighbors.append((chunks[current_chunk_row + 1][current_chunk_column + 1]))

        return neighbors
