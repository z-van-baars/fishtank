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
        self.current_room = current_room
        self.neighbors = []

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
        if predator_x_pos < center_x:
            self.change_x = self.speed
        elif predator_x_pos > center_x:
            self.change_x = -self.speed
        if predator_y_pos < center_y:
            self.change_y = self.speed
        elif predator_y_pos > center_y:
            self.change_y = -self.speed

    def do_thing(self, current_room):
        if self.current_chunk_row is None or \
           self.current_chunk_column is None:
            utilities.place_in_chunk(self, current_room)
        self.eat(current_room)
        self.safety(current_room)


    def reproduce(self, current_room):
        self.coins_collected = 0
        new_goblin = Goblin(self.rect.x + 17, self.rect.y, self.speed, current_room)
        new_goblin.check_bound(current_room)
        utilities.place_in_chunk(new_goblin, current_room)
        current_room.goblins.add(new_goblin)

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
        coin_hit_list = pygame.sprite.spritecollide(self, current_room.coins_list, True)
        for coin in coin_hit_list:
            current_room.coins_list.remove(coin)
            utilities.remove_from_chunk(coin)
            self.coins_collected += 1
            self.lifetime_coins += 1
            self.ticks_without_food = 0
