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
        neighbors.append(self.current_chunk)
        print(current_chunk_row)
        print(current_chunk_column)

        # if you're in the top row of chunks
        if current_chunk_row == 0:
            neighbors.append(chunks[current_chunk_row + 1][current_chunk_column]) # just bottom so far
            # if you're in the first column
            if current_chunk_column == 0:
                neighbors.append(chunks[current_chunk_row][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column + 1]) # add the bottom right and right
            # if you're in the last column
            elif current_chunk_column == len(chunks[0]):
                neighbors.append(chunks[current_chunk_row][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column + 1]) # add the bottom left and left
            # if you're in between
            else:
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row][current_chunk_column + 1]) # add the left, right, bottom left and bottom right

        # if you're in the bottom row of chunks
        elif current_chunk_row == len(chunks):
            neighbors.append(chunks[current_chunk_row - 1][current_chunk_column]) # just the top so far
            # if you're in the first column
            if current_chunk_column == 0:
                neighbors.append(chunks[current_chunk_row][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column + 1]) # add the right and top right
            # if you're in the last column
            elif current_chunk_column == len(chunks[0]):
                neighbors.append(chunks[current_chunk_row][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column - 1]) # add the left and top left
            # if you're in between
            else:
                neighbors.append(chunks[current_chunk_row][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column + 1]) # add the left, right, top left, and top right

        # if you're in between the top and bottom row
        else:
            neighbors.append(chunks[current_chunk_row - 1][current_chunk_column])
            neighbors.append(chunks[current_chunk_row + 1][current_chunk_column]) # just top and bottom so far
            # if you're in the first column
            if current_chunk_column == 0:
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column + 1]) # add the top right and bottom right
            # if you're in the last column
            elif current_chunk_column == len(chunks[0]):
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column - 1]) # add the top left and bottom left
            # if you're in between
            else:

                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column - 1])
                neighbors.append(chunks[current_chunk_row - 1][current_chunk_column + 1])
                neighbors.append(chunks[current_chunk_row + 1][current_chunk_column + 1]) # add the top left, bottom left, top right and top right
        

        return neighbors


    def old_get_neighbors(self, current_chunk_row, current_chunk_column):

        if current_chunk_row > 0:
            neighbors.append(chunks[current_chunk_row - 1]
                                   [current_chunk_column])  # top center
            if current_chunk_column > 0:
                neighbors.append(chunks[current_chunk_row - 1]
                                       [current_chunk_column - 1])  # top left
            elif current_chunk_column < (len(chunks[0]) - 1):
                neighbors.append(chunks[current_chunk_row - 1]
                                       [current_chunk_column + 1])  # top right


        elif current_chunk_row < (len(chunks) - 1):
            neighbors.append(chunks[current_chunk_row + 1]
                                   [current_chunk_column])  # bottom center
            if current_chunk_column > 0:
                neighbors.append(chunks[current_chunk_row + 1]
                                       [current_chunk_column - 1])  # bottom left
            if current_chunk_column < (len(chunks[0]) - 1):
                neighbors.append(chunks[current_chunk_row + 1]
                                       [current_chunk_column + 1])  # bottom right



        if current_chunk_column < (len(chunks[0]) - 1):
            neighbors.append(chunks[current_chunk_row]
                                   [current_chunk_column + 1])  # right

        elif current_chunk_column > 0:
            neighbors.append(chunks[current_chunk_row]
                                   [current_chunk_column - 1])  # left
