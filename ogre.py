import pygame
import utilities
import random
import colors
import goblin
import organism
import wall


class Ogre(organism.Organism):

    def __init__(self, x, y, current_room):
        super().__init__(x, y, current_room, colors.red, 20, 20)
        self.target_goblin = None
        self.speed = 3
        self.goblins_eaten = 0
        self.lifetime_goblins_eaten = 0
        self.change_x = 0
        self.change_y = 0
        self.age = 0
        self.ticks_without_food = 0
        self.food_type = goblin.Goblin

    def dead(self):
        if self.age > 2000:
            self.current_room.ogre_old_age_deaths += 1
            utilities.log("An ogre died of old age")
            self.current_room.goblins_eaten_on_death.append(self.lifetime_goblins_eaten)
            self.current_room.ogre_death_ages.append(self.age)
            self.expire()
            return True
        elif self.ticks_without_food > 300:
            self.current_room.ogre_starvation_deaths += 1
            utilities.log("An Ogre died of starvation")
            self.current_room.goblins_eaten_on_death.append(self.lifetime_goblins_eaten)
            self.current_room.ogre_death_ages.append(self.age)
            self.expire()
            return True

    def do_thing(self):
        self.age += 1
        self.ticks_without_food += 1

        if not self.dead():
            if self.current_chunk_row is None or \
               self.current_chunk_column is None:
                self.place_in_chunk(self.current_room)
            self.chase(self.current_room)
            self.move(self.current_room, self.current_chunk)
            if self.goblins_eaten > 39:
                self.reproduce(self.current_room)

    def collide_x(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        ogre_hit_list = []
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[Ogre], False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_x > 0 and item != self:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and item != self:
                    self.rect.left = item.rect.right
    def collide_y(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        ogre_hit_list = []
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[Ogre], False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_y > 0 and item != self:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and item != self:
                    self.rect.top = item.rect.bottom


    def chase(self, current_room):
        if self.target_goblin is None or \
           self.target_goblin not in current_room.entity_list[goblin.Goblin]:
            self.target_goblin = self.pick_target(self.neighbors)

        prey_x = self.target_goblin.rect.x
        prey_y = self.target_goblin.rect.y

        if prey_x > self.rect.x:
            self.change_x = self.speed
        elif prey_x < self.rect.x:
            self.change_x = -self.speed
        if prey_y > self.rect.y:
            self.change_y = self.speed
        elif prey_y < self.rect.y:
            self.change_y = -self.speed
        goblin_hit_list = []
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[goblin.Goblin], True))
            goblin_hit_list = goblin_hit_list + neighbor_hit_list
        for each in goblin_hit_list:
            self.goblins_eaten += 1
            self.lifetime_goblins_eaten += 1
            self.ticks_without_food = 0
            current_room.deaths_by_ogre += 1
            current_room.coins_on_death.append(each.lifetime_coins)
            current_room.death_ages.append(each.age)
            each.expire()

    def reproduce(self, current_room):
        self.goblins_eaten = 0
        new_ogre = Ogre((self.rect.x + 22), self.rect.y, current_room)
        new_ogre.check_bound(current_room)
        current_room.entity_list[Ogre].add(new_ogre)
        new_ogre.place_in_chunk(new_ogre.current_room)
