import pygame
import random
import math
import statistics

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
blue_grey = (180, 210, 217)
purple = (255, 0, 255)
gold = (255, 187, 0)

key = (255, 0, 128)

logging_on = True


def log(*args, **kwargs):
    if logging_on:
        print(*args, **kwargs)


def distance(a, b, x, y):
    a1 = abs(a - x)
    b1 = abs(b - y)
    c = math.sqrt((a1 * a1) + (b1 * b1))
    return c


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
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([5, 5])
        self.image.fill(gold)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.species = "Coin"

    def __lt__(self, other):
        if self.rect.x < other.rect.x:
            return True
        elif self.rect.y < other.rect.y:
            return True
        else:
            return False


def spawn_org():
    coords = []
    coords.append(random.randrange(21, 779))
    coords.append(random.randrange(21, 579))

    return coords


class Organism(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    age = 0
    ticks_without_food = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.species = None

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def do_thing(self):
        raise NotImplementedError()

    def move(self, walls, goblins, ogres):

        block_hit_list = []
        goblin_hit_list = []
        ogre_hit_list = []
        # X checks
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, goblins, False)
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, ogres, False)

        hit_lists = (block_hit_list, goblin_hit_list, ogre_hit_list)
        for hit_list in hit_lists:

            for item in hit_list:
                if self.change_x > 0 and self.rect.right != item.rect.right:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and self.rect.left != item.rect.left:
                    self.rect.left = item.rect.right
        # Y checks
        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, goblins, False)
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, ogres, False)

        hit_lists = (block_hit_list, goblin_hit_list, ogre_hit_list)
        for hit_list in hit_lists:

            for item in hit_list:
                if self.change_y > 0 and self.rect.top != item.rect.top:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and self.rect.bottom != item.rect.bottom:
                    self.rect.top = item.rect.bottom

    def pick_target(self, possible_targets):
        target_object = None

        def look_within_cutoff(cutoff):
            for target in possible_targets:
                if abs(target.rect.x - self.rect.x) < cutoff and \
                   abs(target.rect.y - self.rect.y) < cutoff:
                    dist = distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
                    yield (dist, target)

        for cutoff in (8, 128):
            distances = look_within_cutoff(cutoff)
            if distances:  # not empty
                distances = sorted(distances)
                try:
                    target_object = distances[0][1]  # 0th (shortest dist), then the 1th element (object itself)
                    break
                except IndexError:
                    continue

        # too far away, just pick one at random
        if target_object is None:
            target_object = random.choice(list(possible_targets))

        assert target_object is not None
        return target_object


class Ogre(Organism):
    def __init__(self, x, y, speed):
        Organism.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_goblin = None
        self.speed = speed
        self.goblins_eaten = 0
        self.lifetime_goblins_eaten = 0
        self.species = "Ogre"

    def do_thing(self, current_room):
        self.chase(current_room)

    # overrides... but should it?
    def pick_target(self, current_room):
        goblin_distances = []
        target_goblin = []

        for goblin in current_room.goblins:
            dist = distance((goblin.rect.x + 7), (goblin.rect.y + 7), (self.rect.x + 10), (self.rect.y + 10))
            goblin_distances.append([dist, (goblin.rect.x, goblin.rect.y)])

        goblin_distances = sorted(goblin_distances)
        target_goblin = goblin_distances[0]
        target_goblin = target_goblin[1]
        self.target_goblin = target_goblin

    def chase(self, current_room):
        prey_x = self.target_goblin[0]
        prey_y = self.target_goblin[1]

        if prey_x > self.rect.x:
            self.change_x = self.speed
        elif prey_x < self.rect.x:
            self.change_x = -self.speed
        if prey_y > self.rect.y:
            self.change_y = self.speed
        elif prey_y < self.rect.y:
            self.change_y = -self.speed
        goblin_hit_list = []
        goblin_hit_list = pygame.sprite.spritecollide(self, current_room.goblins, True)
        for goblin in goblin_hit_list:
            current_room.goblins.remove(goblin)
            self.goblins_eaten += 1
            self.lifetime_goblins_eaten += 1
            self.ticks_without_food = 0
            current_room.deaths_by_ogre += 1
            current_room.coins_on_death.append(goblin.lifetime_coins)
            current_room.death_ages.append(goblin.age)

    def reproduce(self, current_room):
        self.goblins_eaten = 0
        new_ogre = Ogre((self.rect.x + 22), self.rect.y, self.speed)
        current_room.ogres.add(new_ogre)


class Goblin(Organism):
    def __init__(self, x, y, speed):
        Organism.__init__(self)
        self.image = pygame.Surface([15, 15])
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.coins_collected = 0
        self.lifetime_coins = 0
        self.target_coin = None
        self.species = "Goblin"

    def safety(self, current_room):
        center_x = self.rect.x + 7
        center_y = self.rect.y + 7
        safety_left = center_x - 100
        safety_right = center_x + 100
        safety_bottom = center_y + 100
        safety_top = center_y - 100
        for ogre in current_room.ogres:

            predator_x_pos = ogre.rect.x + 10
            predator_y_pos = ogre.rect.y + 10

            if predator_x_pos < safety_right and predator_x_pos > safety_left:
                if predator_y_pos > safety_top and predator_y_pos < safety_bottom:
                    self.run(current_room, center_x, center_y, predator_x_pos, predator_y_pos)

    def run(self, current_room, center_x, center_y, predator_x_pos, predator_y_pos):

        log("a goblin is in danger!")
        if predator_x_pos < center_x:
            self.change_x = self.speed
        elif predator_x_pos > center_x:
            self.change_x = -self.speed
        if predator_y_pos < center_y:
            self.change_y = self.speed
        elif predator_y_pos > center_y:
            self.change_y = -self.speed

    def do_thing(self, current_room):
        self.eat(current_room)
        self.safety(current_room)

    def reproduce(self, current_room):
        self.coins_collected = 0
        new_goblin = Goblin(self.rect.x + 17, self.rect.y, self.speed)
        current_room.goblins.add(new_goblin)

    def eat(self, current_room):
        if self.target_coin is None or \
           self.target_coin not in current_room.coins_list:
            self.target_coin = self.pick_target(current_room.coins_list)

        target_x = self.target_coin.rect.x
        target_y = self.target_coin.rect.y

        # x vector
        if (target_x + 2) > (self.rect.x + 7):
            self.change_x = self.speed
        elif (target_x + 2) < (self.rect.x + 7):
            self.change_x = -self.speed
        else:
            self.change_x = 0

        # y vector
        if (target_y + 2) > (self.rect.y + 7):
            self.change_y = self.speed
        elif (target_y + 2) < (self.rect.y + 7):
            self.change_y = -self.speed
        else:
            self.change_y = 0

        coin_hit_list = []
        coin_hit_list = pygame.sprite.spritecollide(self, current_room.coins_list, True)
        for coin in coin_hit_list:
            current_room.coins_list.remove(coin)
            self.coins_collected += 1
            self.lifetime_coins += 1
            self.ticks_without_food = 0


class Room():
    wall_list = None
    coins_list = None
    goblins = None
    ogres = None
    movingsprites = None
    #goblins stats
    starvation_deaths = 0
    age_deaths = 0
    deaths_by_ogre = 0
    death_ages = []
    average_death_age = 0
    coins_on_death = []
    coins_on_death_average = 0
    #ogre stats
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

        walls = [[0, 0, 20, 600, blue_grey],
                 [780, 0, 20, 600, blue_grey],
                 [20, 0, 760, 20, blue_grey],
                 [20, 580, 760, 20, blue_grey]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

    def update(self):
        if len(self.coins_list) < 60:
            self.spawn_coins(30)

        for ogre in self.ogres:
            ogre.age += 1
            ogre.ticks_without_food += 1
            if ogre.age > 1000:
                self.goblins_eaten_on_death.append(ogre.lifetime_goblins_eaten)
                self.ogre_death_ages.append(1000)
                self.ogres.remove(ogre)
                self.movingsprites.remove(ogre)
                self.age_deaths += 1
                log("An Ogre died of old age")
            elif ogre.ticks_without_food > 700:
                self.goblins_eaten_on_death.append(ogre.lifetime_goblins_eaten)
                self.ogre_death_ages.append(ogre.age)
                self.ogres.remove(ogre)
                self.movingsprites.remove(ogre)
                self.ogre_starvation_deaths += 1
                log("An Ogre died of starvation")
            else:
                ogre.pick_target(self)
                ogre.chase(self)
                ogre.move(self.wall_list, self.goblins, self.ogres)
                if ogre.goblins_eaten > 49:
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
                log("a goblin died of old age")
            elif goblin.ticks_without_food > 200:
                self.coins_on_death.append(goblin.lifetime_coins)
                self.death_ages.append(goblin.age)
                self.goblins.remove(goblin)
                self.movingsprites.remove(goblin)
                self.starvation_deaths += 1
                log("a goblin died of starvation")
            else:
                goblin.do_thing(self)
                goblin.move(self.wall_list, self.goblins, self.ogres)
                if goblin.coins_collected > 15:
                    goblin.reproduce(self)
                self.movingsprites.add(goblin)

    def spawn_coins(self, num_coins):
        for coin in range(num_coins):
            coin = Coin(random.randrange(21, 779), random.randrange(21, 579))
            self.coins_list.add(coin)


def gen_goblin_genes():
        genome = []
        genome.append(random.randrange(2, 3))
        return 2


def gen_ogre_genes():
    genome = []
    genome.append(random.randrange(3, 5))
    return 3


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
    goblin_pop_ticker.fill(green)

    ogre_pop_ticker = pygame.Surface([1, 1])
    ogre_pop_ticker.fill(red)

    tank_bg = pygame.Surface([800, 600])
    tank_bg.fill(black)

    while not done:
        goblin_counter = font.render(str(len(current_room.goblins)), False, black)
        starvation_counter = font.render(str(current_room.starvation_deaths), False, red)
        old_age_counter = font.render(str(current_room.age_deaths), False, red)
        ogre_counter = font.render(str(len(current_room.ogres)), False, black)
        ogre_meals_counter = font.render(str(current_room.deaths_by_ogre), False, black)
        goblin_pop_log.append(len(current_room.goblins))
        ogre_pop_log.append(len(current_room.ogres))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    coordin = spawn_org()
                    genome = gen_goblin_genes()
                    new_goblin = Goblin(coordin[0], coordin[1], genome)
                    current_room.goblins.add(new_goblin)
                    go = True

                elif event.key == pygame.K_o:
                    coordin = spawn_org()
                    genome = gen_ogre_genes()
                    new_ogre = Ogre(coordin[0], coordin[1], genome)
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

    current_room.average_death_age = statistics.mean(current_room.death_ages)
    current_room.coins_on_death_average = statistics.mean(current_room.coins_on_death)
    current_room.ogre_average_death_age = statistics.mean(current_room.ogre_death_ages)
    current_room.ogre_average_goblins_eaten = statistics.mean(current_room.goblins_eaten_on_death)
    print("Average age of Goblins at death: %d" % current_room.average_death_age)
    print("Average lifetime coins collected: %d" % current_room.coins_on_death_average)
    print("Starvation Deaths: %d") % current_room.starvation_deaths
    print("Age Deaths: %d" % current_room.age_deaths)
    print("Deaths by Ogre: %d" % current_room.deaths_by_ogre)
    print("-")
    print("Average age of Ogres at death: %d" % current_room.ogre_average_death_age)
    print("Average number of Goblins eaten: %d" % current_room.ogre_average_goblins_eaten)

    pygame.quit()

main()
