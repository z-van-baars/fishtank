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

logging_on = False
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

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([5, 5])
        self.image.fill(gold)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def do_thing(self):
        raise NotImplementedError()

    def move(self, walls, goblins):

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        goblin_hit_list = pygame.sprite.spritecollide(self, goblins, False)

        # wall X detection
        for block in block_hit_list:
            if self.change_x > 0 and self.rect.right != block.rect.right:
                self.rect.right = block.rect.left
            elif self.change_x < 0 and self.rect.left != block.rect.left:
                self.rect.left = block.rect.right
        # goblin X detection
        for goblin in goblin_hit_list:
            if self.change_x > 0 and self.rect.right != goblin.rect.right:
                self.rect.right = goblin.rect.left
            elif self.change_x < 0 and self.rect.left != goblin.rect.left:
                self.rect.left = goblin.rect.right

        self.rect.y += self.change_y

        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        goblin_hit_list = pygame.sprite.spritecollide(self, goblins, False)
        # block Y detection
        for block in block_hit_list:

            if self.change_y > 0 and self.rect.bottom != block.rect.bottom:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0 and self.rect.top != block.rect.top:
                self.rect.top = block.rect.bottom
        # goblin Y detection
        for goblin in goblin_hit_list:
            if self.change_y > 0 and self.rect.bottom != goblin.rect.bottom:
                self.rect.bottom = goblin.rect.top
            elif self.change_y < 0 and self.rect.top != goblin.rect.top:
                self.rect.top = goblin.rect.bottom


class Ogre(Organism):
    def __init__(self, x, y):
        Organism.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        target_goblin = None
        self.speed = 1

    def do_thing(self, current_room):
        self.chase(current_room)

    def pick_target(self, current_room):
        goblin_distances = []
        target_goblin = []

        for goblin in current_room.goblins:
            dist = distance((goblin.rect.x + 7), (goblin.rect.y + 7), (self.rect.x + 10), (self.rect.y + 10))
            goblin_distances.append([dist, (goblin.rect.x, goblin.rect.y)])

        goblin_distances = sorted(goblin_distances)
<<<<<<< HEAD
        target_goblin = goblin_distances[0]
        target_goblin = target_goblin[1]
=======
        log(goblin_distances[0])
        target_goblin = goblin_distances[0]
        log(target_goblin)
        target_goblin = target_goblin[1]
        log(target_goblin)
>>>>>>> 11253527a30dc58d247d99ddc0e37a102b18ed5b
        self.target_goblin = target_goblin

    def chase(self, current_room):

<<<<<<< HEAD
=======
        log(self.target_goblin)
>>>>>>> 11253527a30dc58d247d99ddc0e37a102b18ed5b
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

    def safety(self, current_room):
        center_x = self.rect.x + 7
        center_y = self.rect.y + 7
        safety_left = center_x - 100
        safety_right = center_x + 100
        safety_bottom = center_y + 100
        safety_top = center_y + 700
        predator_x_pos = current_room.ogre.rect.x + 10
        predator_y_pos = current_room.ogre.rect.y + 10

        if predator_x_pos < safety_right or predator_x_pos > safety_left:
            if predator_y_pos > safety_top or predator_y_pos < safety_bottom:
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

    def pick_target_coin(self, coins_list):
        coin_distances = []
        target_coin = []

        for coin in coins_list:
            dist = distance(coin.rect.x, coin.rect.y, self.rect.x, self.rect.y)
            coin_distances.append([dist, (coin.rect.x, coin.rect.y)])

        coin_distances = sorted(coin_distances)

        target_coin = coin_distances[0]
        target_coin = target_coin[1]
        return target_coin

    def do_thing(self, current_room):
        self.eat(current_room)
        # self.safety(current_room)

    def reproduce(self, current_room):
        self.coins_collected = 0
        new_goblin = Goblin(self.rect.x + 17, self.rect.y, self.speed)
        new_goblin.target_coin = new_goblin.pick_target_coin(current_room.coins_list)
        current_room.goblins.add(new_goblin)

    def eat(self, current_room):

        target_x = self.target_coin[0]
        target_y = self.target_coin[1]

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
            self.target_coin = self.pick_target_coin(current_room.coins_list)
            for goblin in current_room.goblins:
                goblin.target_coin = goblin.pick_target_coin(current_room.coins_list)


class Room():
    wall_list = None
    coins_list = None
    goblins = None
    ogre = None
    movingsprites = None
    starvation_deaths = 0
    age_deaths = 0
    death_ages = []
    average_death_age = 0
    coins_on_death = []
    coins_on_death_average = 0

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.coins_list = pygame.sprite.Group()
        self.goblins = pygame.sprite.Group()
        self.movingsprites = pygame.sprite.Group()


class Room1(Room):
    def __init__(self):
        Room.__init__(self)

        walls = [[0, 0, 20, 800, blue_grey],
                 [780, 0, 20, 800, blue_grey],
                 [20, 0, 760, 20, blue_grey],
                 [20, 580, 760, 20, blue_grey]
                ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

    def update(self):
        if len(self.coins_list) < 30:
            self.spawn_coins(20)

        self.ogre.pick_target(self)
        self.ogre.chase(self)
        self.ogre.move(self.wall_list, self.goblins)
        self.movingsprites.add(self.ogre)
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
            elif goblin.ticks_without_food > 150:
                self.coins_on_death.append(goblin.lifetime_coins)
                self.death_ages.append(goblin.age)
                self.goblins.remove(goblin)
                self.movingsprites.remove(goblin)
                self.starvation_deaths += 1
                log("a goblin died of starvation")
            else:
                goblin.do_thing(self)
                goblin.move(self.wall_list, self.goblins)
                if goblin.coins_collected > 10:
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


def main():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('There\'s always a bigger fish Test')

    rooms = []

    room = Room1()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()
    done = False
    go = False
    font = pygame.font.SysFont('Calibri', 18, True, False)


    while not done:


        goblin_counter = font.render(str(len(current_room.goblins)), False, black)

        starvation_counter = font.render(str(current_room.starvation_deaths), False, red)
        old_age_counter = font.render(str(current_room.age_deaths), False, red)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    coordin = spawn_org()
                    genome = gen_goblin_genes()
                    new_goblin = Goblin(coordin[0], coordin[1], genome)

                    new_goblin.target_coin = new_goblin.pick_target_coin(current_room.coins_list)
                    current_room.goblins.add(new_goblin)

                    coordin = spawn_org()
                    current_room.ogre = Ogre(coordin[0], coordin[1])
                    current_room.ogre.pick_target(current_room)
                    go = True
                elif event.key == pygame.K_SPACE:
                    current_room.spawn_coins(50)

        if go:
            current_room.update()

        screen.fill(black)

        current_room.movingsprites.draw(screen)
        current_room.wall_list.draw(screen)
        current_room.coins_list.draw(screen)
        screen.blit(goblin_counter, [1, 1])
        screen.blit(starvation_counter, [100, 1])
        screen.blit(old_age_counter, [200, 1])
        pygame.display.flip()
        clock.tick(60)

<<<<<<< HEAD
    current_room.average_death_age = statistics.mean(current_room.death_ages)
    current_room.coins_on_death_average = statistics.mean(current_room.coins_on_death)
    print("Average age at death: %d" % current_room.average_death_age)
    print("Average lifetime coins collected: %d" % current_room.coins_on_death_average)
    print("Starvation Deaths: ")
    print(current_room.starvation_deaths)
    print("Age Deaths: ")
    print(current_room.age_deaths)
=======
    log("Starvation Deaths: ")
    log(current_room.starvation_deaths)
    log("Age Deaths: ")
    log(current_room.age_deaths)
>>>>>>> 11253527a30dc58d247d99ddc0e37a102b18ed5b
    pygame.quit()

main()
