import pygame
import random
import colors
import utilities
import item
import organism
import ogre
import goblin

class Coin(item.Item):
    def __init__(self, x, y, current_room):
        pygame.sprite.Sprite.__init__(self)
        item.Item.__init__(self, x, y, current_room, colors.gold, 5, 5)

    def __lt__(self, other):
        if self.rect.x < other.rect.x:
            return True
        elif self.rect.y < other.rect.y:
            return True
        else:
            return False


class Chunk():

    def __init__(self, x_pos, y_pos, chunk_width, chunk_height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.left = x_pos
        self.right = x_pos + chunk_width
        self.top = y_pos
        self.bottom = y_pos + chunk_height
        self.entity_list = {}
        self.entity_list[Coin] = pygame.sprite.Group()
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        self.entity_list[ogre.Ogre] = pygame.sprite.Group()
        self.entity_list[Wall] = pygame.sprite.Group()


class Wall(item.Item):
    def __init__(self, x, y, current_room, color, width, height):
        pygame.sprite.Sprite.__init__(self)
        item.Item.__init__(self, x, y, current_room, color, width, height)

class Room():
    def __init__(self):
        self.wall_list = None
        self.coins_list = None
        self.goblins = None
        self.ogres = None
        self.chunks = []
        self.entity_list = {}
        self.entity_list[Coin] = pygame.sprite.Group()
        self.entity_list[goblin.Goblin] = pygame.sprite.Group()
        self.entity_list[ogre.Ogre] = pygame.sprite.Group()
        self.entity_list[Wall] = pygame.sprite.Group()
        self.entity_list['movingsprites'] = pygame.sprite.Group()
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

    def __init__(self, tank_width, tank_height):
        Room.__init__(self)

        self.create_chunks(tank_width, tank_height)

        walls = [[0, 0, self, colors.blue_grey, 20, 600],
                 [780, 0, self, colors.blue_grey, 20, 600],
                 [20, 0, self, colors.blue_grey,  760, 20,],
                 [20, 580, self, colors.blue_grey, 760, 20,]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4], item[5])
            self.entity_list[Wall].add(wall)
        

    def create_chunks(self, tank_width, tank_height):
        # chunk_row0 = [[20, 20],[115, 20],[210, 20],[305, 20],[400, 20],[495, 20],[590, 20],[685, 20]]
        # chunk_row1 = [[20, 100],[115, 100],[210, 100],[305, 100],[400, 100],[495, 100],[590, 100],[685, 100]]
        # chunk_row2 = [[20, 180],[115, 180],[210, 180],[305, 180],[400, 180],[495, 180],[590, 180],[685, 180]]
        # chunk_row3 = [[20, 260],[115, 260],[210, 260],[305, 260],[400, 260],[495, 260],[590, 260],[685, 260]]
        # chunk_row4 = [[20, 340],[115, 340],[210, 340],[305, 340],[400, 340],[495, 340],[590, 340],[685, 340]]
        # chunk_row5 = [[20, 420],[115, 420],[210, 420],[305, 420],[400, 420],[495, 420],[590, 420],[685, 420]]
        # chunk_row6 = [[20, 500],[115, 500],[210, 500],[305, 500],[400, 500],[495, 500],[590, 500],[685, 500]]
        # chunk_rows = [chunk_row0, chunk_row1, chunk_row2, chunk_row3, chunk_row4, chunk_row5, chunk_row6]

        # for row in range(len(chunk_rows)):
            # new_chunk_row = []
            # for item in range(len(chunk_rows[row])):
                # new_chunk = Chunk(chunk_rows[row][item][0], chunk_rows[row][item][1])
                # new_chunk_row.append(new_chunk)
            # self.chunk_rows.append(new_chunk_row)

        chunk_width = 100
        chunk_height = 100

        self.chunks = []
        y = 0
        while y + chunk_height < tank_height:
            this_row = []
            x = 0
            while x + chunk_width <= tank_width:
                this_chunk = Chunk(x, y, chunk_width, chunk_height)
                this_row.append(this_chunk)
                x += chunk_width
            self.chunks.append(this_row)
            y += chunk_height
        print(len(self.chunks))
        print(len(self.chunks[0]))


    def update(self):
        
        if len(self.entity_list[Coin]) < 60:
            self.spawn_coins(30)

        for ogre in self.entity_list[ogre.Ogre]:
            ogre.do_thing()

        for goblin in self.entity_list[goblin.Goblin]:
            goblin.do_thing()



    def spawn_coins(self, num_coins):
        for coin in range(num_coins):
            coin_x = random.randrange(30, 770)
            coin_y = random.randrange(30, 570)
            coin = Coin(coin_x, coin_y, self)
            self.entity_list[Coin].add(coin)
            coin.place_in_chunk(self)
