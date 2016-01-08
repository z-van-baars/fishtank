import random
import math
import pygame
import colors
import utilities


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
            # places creature back inside play area if it bugs out
            if self.rect.left < 20:
                self.rect.left = 20
            if self.rect.right > 780:
                self.rect.right = 780

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
            if self.rect.top < 20:
                self.rect.top = 20
            if self.rect.bottom > 580:
                self.rect.bottom = 580

    def pick_target(self, possible_targets):
        target_object = None

        def look_within_cutoff(cutoff):
            for target in possible_targets:
                if abs(target.rect.x - self.rect.x) < cutoff and \
                   abs(target.rect.y - self.rect.y) < cutoff:
                    dist = utilities.distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
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
        self.image.fill(colors.red)
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
            dist = utilities.distance((goblin.rect.x + 7), (goblin.rect.y + 7), (self.rect.x + 10), (self.rect.y + 10))
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
        self.image.fill(colors.green)
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

        utilities.log("a goblin is in danger!")
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

