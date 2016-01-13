import pygame
import random
import colors
import utilities
import ogre
import hut
import goblin
import coin
import pit
import wall


class Chunk():

    def __init__(self, x_pos, y_pos, chunk_width, chunk_height):
        self.left = x_pos
        self.right = x_pos + chunk_width - 1
        self.top = y_pos
        self.bottom = y_pos + chunk_height - 1
        self.entity_list = {}
        self.entity_list[coin.Coin] = pygame.sprite.Group()
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        self.entity_list[ogre.Ogre] = pygame.sprite.Group()
        self.entity_list[wall.Wall] = pygame.sprite.Group()
        self.entity_list[hut.Hut] = pygame.sprite.Group()
        self.entity_list[pit.Pit] = pygame.sprite.Group()


class Room(object):

    def __init__(self):
        self.wall_list = None
        self.coins_list = None
        self.goblins = None
        self.ogres = None
        self.chunks = []
        self.entity_list = {}
        self.entity_list[coin.Coin] = pygame.sprite.Group()
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        self.entity_list[ogre.Ogre] = pygame.sprite.Group()
        self.entity_list[wall.Wall] = pygame.sprite.Group()
        self.entity_list[hut.Hut] = pygame.sprite.Group()
        self.entity_list[pit.Pit] = pygame.sprite.Group()
        # goblins stats
        self.starvation_deaths = 0
        self.age_deaths = 0
        self.deaths_by_ogre = 0
        self.death_ages = []
        self.average_death_age = 0
        self.coins_on_death = []
        self.coins_on_death_average = 0
        # ogre stats
        self.ogre_starvation_deaths = 0
        self.ogre_old_age_deaths = 0
        self.goblins_eaten_on_death = []
        self.ogre_death_ages = []
        self.ogre_average_death_age = 0
        self.ogre_average_goblins_eaten = 0


class Room1(Room):

    def __init__(self, tank_width, tank_height, num_cols, num_rows):
        super().__init__()

        self.create_chunks(tank_width, tank_height, num_cols, num_rows)

        walls = [
            [0, 0, self, colors.blue_grey, 20, 600],
            [780, 0, self, colors.blue_grey, 20, 600],
            [20, 0, self, colors.blue_grey,  760, 20],
            [20, 580, self, colors.blue_grey, 760, 20],
        ]

        for each in walls:
            self.entity_list[wall.Wall].add(wall.Wall(each[0], each[1], each[2], each[3], each[4], each[5]))

    def create_chunks(self, tank_width, tank_height, num_cols, num_rows):
        if tank_width % num_cols != 0 or tank_height % num_rows != 0:
            raise ValueError("Width and height must be evenly divisible by columns and rows\n" +
                             "Width: {} Columns: {}\n".format(tank_width, num_cols) +
                             "Height: {} Rows: {}".format(tank_height, num_rows))
        chunk_width = tank_width / num_cols
        chunk_height = tank_height / num_rows

        self.chunks = []
        for ii in range(num_rows):
            curr_row = []
            for jj in range(num_cols):
                curr_row.append(
                    Chunk(jj * chunk_width, ii * chunk_height,
                          chunk_width, chunk_height))
            self.chunks.append(curr_row)

        # utilities.log(len(self.chunks))
        # utilities.log(len(self.chunks[0]))

    def update(self):

        for each in self.entity_list[ogre.Ogre]:
            each.do_thing()

        for each in self.entity_list[goblin.Goblin]:
            each.do_thing()

        for each in self.entity_list[pit.Pit]:
            if each.coins > 15:
                each.spawn_goblin()

    def spawn_coins(self, num_coins):
        for each in range(num_coins):
            coin_x = random.randrange(30, 770)
            coin_y = random.randrange(30, 570)
            cc = coin.Coin(coin_x, coin_y, self)

            self.entity_list[coin.Coin].add(cc)
            cc.place_in_chunk(self)

            
