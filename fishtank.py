import pygame
import random
import math
import statistics
import organism
import goblin
import ogre
import utilities
import colors


# To Do
# =====
# - Speed up coin searching / target selection
# - Switch to vectors rather than X Y values

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.species = "Wall"


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
        self.current_room = current_room

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
        self.left = self.top_left_x
        self.right = self.top_left_x + self.width
        self.top = self.top_left_y
        self.bottom = self.top_left_y + self.height
        self.coins_list = pygame.sprite.Group()
        self.goblins_list = pygame.sprite.Group()
        self.ogres_list = pygame.sprite.Group()


class Room():
    wall_list = None
    coins_list = None
    goblins = None
    ogres = None
    movingsprites = None
    chunks = []
    chunk_dict = {}
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

        walls = [[0, 0, 20, 600, colors.blue_grey],
                 [780, 0, 20, 600, colors.blue_grey],
                 [20, 0, 760, 20, colors.blue_grey],
                 [20, 580, 760, 20, colors.blue_grey]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        self.create_chunks()

    def create_chunks(self):
        chunk_coords = []
        chunk_no = 0

        for y in range(7):
            for x in range(8):
                chunk_x = x
                chunk_y = y

                chunk_y *= 95
                chunk_y += 20
                chunk_x *= 80
                chunk_x += 20

                chunk_coords.append([chunk_y, chunk_x])

        for chunk in chunk_coords:
            new_chunk = Chunk(chunk[0], chunk[1])
            self.chunks.append(new_chunk)

        for chunk in self.chunks:
            self.chunk_dict[chunk_no] = self.chunks[chunk_no]
            chunk_no += 1

    def update(self):
        if len(self.coins_list) < 60:
            self.spawn_coins(30)

        for ogre in self.ogres:
            ogre.age += 1
            ogre.ticks_without_food += 1
            if ogre.age > 5000:
                self.goblins_eaten_on_death.append(ogre.lifetime_goblins_eaten)
                self.ogre_death_ages.append(5000)
                self.ogres.remove(ogre)
                self.movingsprites.remove(ogre)
                self.age_deaths += 1
                utilities.log("An Ogre died of old age")
            elif ogre.ticks_without_food > 800:
                self.goblins_eaten_on_death.append(ogre.lifetime_goblins_eaten)
                self.ogre_death_ages.append(ogre.age)
                self.ogres.remove(ogre)
                self.movingsprites.remove(ogre)
                self.ogre_starvation_deaths += 1
                utilities.log("An Ogre died of starvation")
            else:
                ogre.pick_target(self)
                ogre.do_thing(self)
                ogre.move(ogre.current_room)
                if ogre.goblins_eaten > 39:
                    ogre.reproduce(self)
                self.movingsprites.add(ogre)

        for goblin in self.goblins:
            goblin.age += 1
            goblin.ticks_without_food += 1
            if goblin.age > 2000:
                self.coins_on_death.append(goblin.lifetime_coins)
                self.death_ages.append(2000)
                self.goblins.remove(goblin)
                self.movingsprites.remove(goblin)
                self.age_deaths += 1
                utilities.log("a goblin died of old age")
            elif goblin.ticks_without_food > 200:
                self.coins_on_death.append(goblin.lifetime_coins)
                self.death_ages.append(goblin.age)
                self.goblins.remove(goblin)
                self.movingsprites.remove(goblin)
                self.starvation_deaths += 1
                utilities.log("a goblin died of starvation")
            else:
                goblin.do_thing(self)
                goblin.move(goblin.current_room)
                if goblin.coins_collected > 15:
                    goblin.reproduce(self)
                self.movingsprites.add(goblin)

    def spawn_coins(self, num_coins):
        for coin in range(num_coins):
            coin = Coin(random.randrange(21, 779), random.randrange(21, 579), self)
            self.coins_list.add(coin)
            utilities.place_in_chunk(coin, self)


def graph_pop(screen, time, current_room, goblin_pop_ticker, ogre_pop_ticker):
    goblin_pop = len(current_room.goblins)
    ogre_pop = len(current_room.ogres)
    goblin_pop = round(goblin_pop / 2)
    ogre_pop = round(ogre_pop)

    graph_time = round(time / 60)

    screen.blit(ogre_pop_ticker, [graph_time, (799 - ogre_pop)])
    screen.blit(goblin_pop_ticker, [graph_time, (799 - goblin_pop)])


def main():
    pygame.init()
    screen = pygame.display.set_mode([800, 800])
    pygame.display.set_caption('There\'s always a bigger fish Test')

    rooms = []
    rooms.append(Room1())

    goblin_pop_log = []
    ogre_pop_log = []
    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()
    done = False
    go = False
    time = 0
    font = pygame.font.SysFont('Calibri', 18, True, False)
    goblin_pop_ticker = pygame.Surface([1, 1])
    goblin_pop_ticker.fill(colors.green)

    ogre_pop_ticker = pygame.Surface([1, 1])
    ogre_pop_ticker.fill(colors.red)

    tank_bg = pygame.Surface([800, 600])
    tank_bg.fill(colors.black)

    while not done:
        goblin_counter = font.render(str(len(current_room.goblins)), False, colors.black)
        starvation_counter = font.render(str(current_room.starvation_deaths), False, colors.red)
        old_age_counter = font.render(str(current_room.age_deaths), False, colors.red)
        ogre_counter = font.render(str(len(current_room.ogres)), False, colors.black)
        ogre_meals_counter = font.render(str(current_room.deaths_by_ogre), False, colors.black)
        goblin_pop_log.append(len(current_room.goblins))
        ogre_pop_log.append(len(current_room.ogres))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    coordin = utilities.spawn_org()
                    genome = utilities.gen_goblin_genes()
                    new_goblin = goblin.Goblin(coordin[0], coordin[1], genome, None, current_room)
                    utilities.place_in_chunk(new_goblin, current_room)
                    current_room.goblins.add(new_goblin)
                    go = True

                elif event.key == pygame.K_o:
                    coordin = utilities.spawn_org()
                    genome = utilities.gen_ogre_genes()
                    new_ogre = ogre.Ogre(coordin[0], coordin[1], genome, None, current_room)
                    utilities.place_in_chunk(new_ogre, current_room)
                    new_ogre.pick_target(current_room)
                    current_room.ogres.add(new_ogre)
                    go = True

                elif event.key == pygame.K_SPACE:
                    current_room.spawn_coins(100)

        if go:
            current_room.update()

        graph_pop(screen, time, current_room, goblin_pop_ticker, ogre_pop_ticker)
        screen.blit(tank_bg, [0, 0])
        current_room.movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        current_room.coins_list.draw(screen)
        screen.blit(goblin_counter, [1, 1])
        screen.blit(starvation_counter, [100, 1])
        screen.blit(old_age_counter, [200, 1])
        screen.blit(ogre_counter, [500, 1])
        screen.blit(ogre_meals_counter, [550, 1])

        pygame.display.flip()
        clock.tick(60)
        time += 1

    if current_room.death_ages:
        current_room.average_death_age = statistics.mean(current_room.death_ages)
    else:
        current_room.average_death_age = 0
    if current_room.coins_on_death:
        current_room.coins_on_death_average = statistics.mean(current_room.coins_on_death)
    else:
        current_room.coins_on_death_average = 0
    if current_room.ogre_death_ages:
        current_room.ogre_average_death_age = statistics.mean(current_room.ogre_death_ages)
    else:
        current_room.ogre_average_death_age = 0
    if current_room.goblins_eaten_on_death:
        current_room.ogre_average_goblins_eaten = statistics.mean(current_room.goblins_eaten_on_death)
    else:
        current_room.ogre_average_goblins_eaten = 0

    print("\n" * 5)
    print("Average age of Goblins at death: %s" % str(current_room.average_death_age))
    print("Average lifetime coins collected: %s" % str(current_room.coins_on_death_average))
    print("Starvation Deaths: %s" % str(current_room.starvation_deaths))
    print("Age Deaths: %s" % str(current_room.age_deaths))
    print("Deaths by Ogre: %s" % str(current_room.deaths_by_ogre))
    print("-")
    print("Average age of Ogres at death: %s" % str(current_room.ogre_average_death_age))
    print("Average number of Goblins eaten: %s" % str(current_room.ogre_average_goblins_eaten))

    pygame.quit()

main()
