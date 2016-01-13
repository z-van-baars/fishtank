import pygame
import utilities
import colors
import organism
import ogre
import coin
import wall
import hut
import pit

pygame.init()
pygame.display.set_caption("There's always a bigger fish")
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])

goblin_img = pygame.image.load("art/goblin.png").convert()
goblin_img.set_colorkey(colors.key)


class Goblin(organism.Organism):


    def __init__(self, x, y, current_room):
        super().__init__((x - 7), (y - 7), current_room, colors.green, 15, 15)
        self.image = goblin_img
        self.speed = 2
        self.coins_collected = 0
        self.lifetime_coins = 0
        self.target_coin = None
        self.max_age = 2000
        self.max_hunger = 300
        self.change_x = 0
        self.change_y = 0
        self.age = 0
        self.ticks_without_food = 0
        self.food_type = coin.Coin
        self.pit = None

    def safety(self, current_room):
        center_x = self.rect.x + 7
        center_y = self.rect.y + 7
        safety_left = center_x - 50
        safety_right = center_x + 50
        safety_bottom = center_y + 50
        safety_top = center_y - 50

        for neighbor_chunk in self.neighbors:
            for each in neighbor_chunk.entity_list[ogre.Ogre]:
                predator_x_pos = each.rect.x + 10
                predator_y_pos = each.rect.y + 10
                if predator_x_pos < safety_right and predator_x_pos > safety_left:
                    if predator_y_pos > safety_top and predator_y_pos < safety_bottom:
                        self.run(current_room, center_x, center_y, predator_x_pos, predator_y_pos)

    def find_pit(self):
        possible_homes = []
        for possible_home in self.current_room.entity_list[pit.Pit]:
            home_dist = utilities.distance(possible_home.rect.x, possible_home.rect.y, self.rect.x, self.rect.y)
            possible_homes.append((home_dist, possible_home))
        possible_homes = sorted(possible_homes)
        self.pit = possible_homes[0][1]

    def run(self, current_room, center_x, center_y, predator_x_pos, predator_y_pos):
        if predator_x_pos < center_x:
            self.change_x = self.speed
        elif predator_x_pos > center_x:
            self.change_x = -self.speed
        if predator_y_pos < center_y:
            self.change_y = self.speed
        elif predator_y_pos > center_y:
            self.change_y = -self.speed
        self.target_coin = self.pick_target(self.neighbors, self.current_room)

    def dead(self):
        if self.age > 2000:
            self.current_room.age_deaths += 1
            utilities.log("a goblin died of old age")
            self.current_room.coins_on_death.append(self.lifetime_coins)
            self.current_room.death_ages.append(self.age)
            self.expire()
            return True
        elif self.ticks_without_food > 400:
            self.current_room.starvation_deaths += 1
            utilities.log("a goblin died of starvation")
            self.current_room.coins_on_death.append(self.lifetime_coins)
            self.current_room.death_ages.append(self.age)
            self.expire()
            self.kill()
            return True

    def go_home(self):
        home_x = self.pit.rect.x + 15
        home_y = self.pit.rect.y + 15

        home_dist = utilities.distance((home_x), (home_y), self.rect.x, self.rect.y)
        if home_dist > 38:
            changes = utilities.get_vector(self, home_x, home_y, self.rect.x + 10, self.rect.y + 10)
            self.change_x = changes[0]
            self.change_y = changes[1]
        else:
            self.give_coins()

        self.coin_pickup(self.current_room)

    def give_coins(self):
        self.pit.coins += self.coins_collected
        self.pit.lifetime_coins += self.coins_collected
        self.coins_collected = 0
        self.ticks_without_food = 0
        self.change_x = 0
        self.change_y = 0

    def coin_pickup(self, current_room):

        coin_hit_list = pygame.sprite.spritecollide(self, self.current_chunk.entity_list[coin.Coin], True)
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[coin.Coin], True))
            coin_hit_list = coin_hit_list + neighbor_hit_list
        for each in coin_hit_list:
            each.kill()
            self.coins_collected += 1
            self.lifetime_coins += 1
            self.ticks_without_food = 0

    def do_thing(self):
        if self.current_chunk_row is None or \
           self.current_chunk_column is None:
            self.place_in_chunk(self, self.current_room)
        if self.pit is None:
            if self.current_room.entity_list[pit.Pit]:
                self.find_pit()

        self.age += 1
        self.ticks_without_food += 1

        if not self.dead():
            if self.coins_collected >= 10 and self.pit is not None:
                self.go_home()
            else:
                if self.current_room.entity_list[coin.Coin]:
                    self.eat(self.current_room)
            self.safety(self.current_room)
            self.move(self.current_room, self.current_chunk)

    def collide_x(self, current_room, current_chunk):
        # pygame.sprite.spritecollide(self, current_room.entity_list[Goblin], False)
        goblin_hit_list = []
        pit_hit_list = []
        hut_hit_list = []
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        for neighbor in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, neighbor.entity_list[Goblin], False))
            goblin_hit_list += neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, neighbor.entity_list[hut.Hut], False)
            goblin_hit_list += neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, neighbor.entity_list[pit.Pit], False)
            pit_hit_list += neighbor_hit_list
        hit_lists = (wall_hit_list, goblin_hit_list, hut_hit_list, pit_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_x > 0 and item != self:
                    self.rect.right = item.rect.left - 1
                elif self.change_x < 0 and item != self:
                    self.rect.left = item.rect.right + 1

    def collide_y(self, current_room, current_chunk):
        # pygame.sprite.spritecollide(self, current_room.entity_list[Goblin], False)
        goblin_hit_list = []
        hut_hit_list = []
        pit_hit_list = []
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        for neighbor in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, neighbor.entity_list[Goblin], False))
            goblin_hit_list + neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, neighbor.entity_list[hut.Hut], False)
            hut_hit_list + neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, neighbor.entity_list[pit.Pit], False)
            pit_hit_list += neighbor_hit_list
        hit_lists = (wall_hit_list, goblin_hit_list, hut_hit_list, pit_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_y > 0 and item != self:
                    self.rect.bottom = item.rect.top - 1
                elif self.change_y < 0 and item != self:
                    self.rect.top = item.rect.bottom + 1

    def reproduce(self, current_room):
        self.coins_collected = 0
        new_goblin = Goblin(self.rect.x + 17, self.rect.y, current_room)
        new_goblin.check_bound(current_room)
        new_goblin.place_in_chunk(current_room)
        current_room.entity_list[Goblin].add(new_goblin)

    def eat(self, current_room):
        if self.target_coin is None or \
           self.target_coin not in current_room.entity_list[coin.Coin]:
            self.target_coin = self.pick_target(self.neighbors, self.current_room)

        changes = utilities.get_vector(self, self.target_coin.rect.x + 2, self.target_coin.rect.y + 2, self.rect.x + 7, self.rect.y + 7)
        self.change_x = changes[0]
        self.change_y = changes[1]
        # pygame.sprite.spritecollide(self, self.current_room.entity_list[coin.Coin], True)
        self.coin_pickup(self.current_room)
