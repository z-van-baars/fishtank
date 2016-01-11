import pygame
import utilities
import colors
import organism


class Goblin(organism.Organism):
    change_x = 0
    change_y = 0
    age = 0
    ticks_without_food = 0

    def __init__(self, x, y, speed, current_room):
        organism.Organism.__init__(self)
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
        self.current_chunk_row = None
        self.current_chunk_column = None
        self.current_chunk = None
        self.current_room = current_room
        self.neighbors = []
        self.max_age = 2000
        self.max_hunger = 300

    def safety(self, current_room):
        center_x = self.rect.x + 7
        center_y = self.rect.y + 7
        safety_left = center_x - 100
        safety_right = center_x + 100
        safety_bottom = center_y + 100
        safety_top = center_y - 100
        for ogre in self.current_chunk.ogres_list:
            predator_x_pos = ogre.rect.x + 10
            predator_y_pos = ogre.rect.y + 10
            if predator_x_pos < safety_right and predator_x_pos > safety_left:
                if predator_y_pos > safety_top and predator_y_pos < safety_bottom:
                    self.run(current_room, center_x, center_y, predator_x_pos, predator_y_pos)

        for neighbor_chunk in self.neighbors:
            for ogre in neighbor_chunk.ogres_list:
                predator_x_pos = ogre.rect.x + 10
                predator_y_pos = ogre.rect.y + 10
                if predator_x_pos < safety_right and predator_x_pos > safety_left:
                    if predator_y_pos > safety_top and predator_y_pos < safety_bottom:
                        self.run(current_room, center_x, center_y, predator_x_pos, predator_y_pos)

    def run(self, current_room, center_x, center_y, predator_x_pos, predator_y_pos):
        if predator_x_pos < center_x:
            self.change_x = self.speed
        elif predator_x_pos > center_x:
            self.change_x = -self.speed
        if predator_y_pos < center_y:
            self.change_y = self.speed
        elif predator_y_pos > center_y:
            self.change_y = -self.speed

    def dead(self):
        if self.age > 2000:
            self.current_room.age_deaths += 1
            utilities.log("a goblin died of old age")
            self.current_room.coins_on_death.append(self.lifetime_coins)
            self.current_room.death_ages.append(self.age)
            self.current_room.goblins.remove(self)
            self.current_chunk.goblins_list.remove(self)
            self.current_room.movingsprites.remove(self)
            return True
        elif self.ticks_without_food > 300:
            self.current_room.starvation_deaths += 1
            utilities.log("a goblin died of starvation")
            self.current_room.coins_on_death.append(self.lifetime_coins)
            self.current_room.death_ages.append(self.age)
            self.current_room.goblins.remove(self)
            self.current_chunk.goblins_list.remove(self)
            self.current_room.movingsprites.remove(self)
            return True

    def do_thing(self):
        if self.current_chunk_row is None or \
           self.current_chunk_column is None:
            utilities.place_in_chunk(self, self.current_room)

        self.age += 1
        self.ticks_without_food += 1

        if not self.dead():
            self.safety(self.current_room)
            self.eat(self.current_room)
            self.move(self.current_room, self.current_chunk)
            if self.coins_collected > 15:
                self.reproduce(self.current_room)

    def collide_x(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        goblin_hit_list = pygame.sprite.spritecollide(self, current_chunk.goblins_list, False)
        for neighbor in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, neighbor.goblins_list, False))
            goblin_hit_list = goblin_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, goblin_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_x > 0 and item != self:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and item != self:
                    self.rect.left = item.rect.right

    def collide_y(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        goblin_hit_list = pygame.sprite.spritecollide(self, current_chunk.goblins_list, False)
        for neighbor in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, neighbor.goblins_list, False))
            goblin_hit_list = goblin_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, goblin_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_y > 0 and item != self:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and item != self:
                    self.rect.top = item.rect.bottom

    def reproduce(self, current_room):
        self.coins_collected = 0
        new_goblin = Goblin(self.rect.x + 17, self.rect.y, self.speed, current_room)
        
        new_goblin.check_bound(current_room)
        utilities.place_in_chunk(new_goblin, current_room)
        current_room.goblins.add(new_goblin)
        current_room.movingsprites.add(new_goblin)

    def eat(self, current_room):
        if self.target_coin is None or \
           self.target_coin not in current_room.coins_list:
            self.target_coin = self.pick_target(self.neighbors, self.current_chunk_row, self.current_chunk_column)

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
        coin_hit_list = pygame.sprite.spritecollide(self, self.current_chunk.coins_list, True)
        for chunk in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.coins_list, True))
            coin_hit_list = coin_hit_list + neighbor_hit_list
        for coin in coin_hit_list:
            current_room.coins_list.remove(coin)
            coin.current_chunk.coins_list.remove(coin)
            self.coins_collected += 1
            self.lifetime_coins += 1
            self.ticks_without_food = 0
