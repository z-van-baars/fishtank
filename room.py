import pygame
import random
import colors
import utilities

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, current_room):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 5])
        self.image.fill(colors.gold)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.species = "Coin"
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


class Chunk():

    def __init__(self, x_pos, y_pos):
        self.top_left_x = x_pos
        self.top_left_y = y_pos
        self.width = 95
        self.height = 80
        self.left = x_pos
        self.right = x_pos + 95
        self.top = y_pos
        self.bottom = y_pos + 80
        self.coins_list = pygame.sprite.Group()
        self.goblins_list = pygame.sprite.Group()
        self.ogres_list = pygame.sprite.Group()
        self.walls_list = pygame.sprite.Group()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.species = "Wall"
        self.current_chunk_row = None
        self.current_chunk_column = None
        self.current_chunk = None

class Room():

    wall_list = None
    coins_list = None
    goblins = None
    ogres = None
    movingsprites = None
    chunk_rows = []
    # goblins stats
    starvation_deaths = 0
    age_deaths = 0
    deaths_by_ogre = 0
    death_ages = []
    average_death_age = 0
    coins_on_death = []
    coins_on_death_average = 0
    # ogre stats
    ogre_starvation_deaths = 0
    ogre_old_age_deaths = 0
    goblins_eaten_on_death = []
    ogre_death_ages = []
    ogre_average_death_age = 0
    ogre_average_goblins_eaten = 0

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coins_list = pygame.sprite.Group()
        self.goblins = pygame.sprite.Group()
        self.movingsprites = pygame.sprite.Group()
        self.ogres = pygame.sprite.Group()


class Room1(Room):

    def __init__(self):
        Room.__init__(self)

        self.create_chunks()

        walls = [[0, 0, 20, 600, colors.blue_grey],
                 [780, 0, 20, 600, colors.blue_grey],
                 [20, 0, 760, 20, colors.blue_grey],
                 [20, 580, 760, 20, colors.blue_grey]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        

    def create_chunks(self):
        chunk_row0 = [[20, 20],[115, 20],[210, 20],[305, 20],[400, 20],[495, 20],[590, 20],[685, 20]]
        chunk_row1 = [[20, 100],[115, 100],[210, 100],[305, 100],[400, 100],[495, 100],[590, 100],[685, 100]]
        chunk_row2 = [[20, 180],[115, 180],[210, 180],[305, 180],[400, 180],[495, 180],[590, 180],[685, 180]]
        chunk_row3 = [[20, 260],[115, 260],[210, 260],[305, 260],[400, 260],[495, 260],[590, 260],[685, 260]]
        chunk_row4 = [[20, 340],[115, 340],[210, 340],[305, 340],[400, 340],[495, 340],[590, 340],[685, 340]]
        chunk_row5 = [[20, 420],[115, 420],[210, 420],[305, 420],[400, 420],[495, 420],[590, 420],[685, 420]]
        chunk_row6 = [[20, 500],[115, 500],[210, 500],[305, 500],[400, 500],[495, 500],[590, 500],[685, 500]]
        chunk_rows = [chunk_row0, chunk_row1, chunk_row2, chunk_row3, chunk_row4, chunk_row5, chunk_row6]

        for row in range(len(chunk_rows)):
            new_chunk_row = []
            for item in range(len(chunk_rows[row])):
                new_chunk = Chunk(chunk_rows[row][item][0], chunk_rows[row][item][1])
                new_chunk_row.append(new_chunk)
            self.chunk_rows.append(new_chunk_row)

    def update(self):
        self.movingsprites = None
        self.movingsprites = pygame.sprite.Group()
        if len(self.coins_list) < 60:
            self.spawn_coins(30)

        for ogre in self.ogres:
            ogre.do_thing()
        self.movingsprites.add(self.ogres)
        for goblin in self.goblins:
            goblin.do_thing()
        self.movingsprites.add(self.goblins)


    def spawn_coins(self, num_coins):
        for coin in range(num_coins):
            coin_x = random.randrange(30, 770)
            coin_y = random.randrange(30, 570)
            coin = Coin(coin_x, coin_y, self)
            self.coins_list.add(coin)
            utilities.place_in_chunk(coin, self)
