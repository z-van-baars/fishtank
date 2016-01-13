import pygame
import utilities
import random
import colors
import goblin
import organism
import wall
import hut

pygame.init()
pygame.display.set_caption("There's always a bigger fish")
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode([screen_width, screen_height])
ogre_img = pygame.image.load("art/ogre.png")
ogre_img.set_colorkey(colors.key)


class Ogre(organism.Organism):

    def __init__(self, x, y, current_room):
        super().__init__((x - 10), (y - 10), current_room, colors.red, 20, 20)
        self.image = ogre_img
        self.target_goblin = None
        self.speed = 3
        self.goblins_eaten = 0
        self.lifetime_goblins_eaten = 0
        self.change_x = 0
        self.change_y = 0
        self.age = 0
        self.ticks_without_food = 0
        self.food_type = goblin.Goblin
        self.home_hut = None

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
        if not self.home_hut:
            if self.current_room.entity_list[hut.Hut]:
                self.find_home()
        self.age += 1
        self.ticks_without_food += 1

        if not self.dead():
            if self.current_chunk_row is None or \
               self.current_chunk_column is None:
                self.place_in_chunk(self.current_room)
            if self.current_room.entity_list[goblin.Goblin]:
                self.chase(self.current_room)
            else:
                self.idle()
            self.move(self.current_room, self.current_chunk)
            if self.goblins_eaten > 39:
                self.reproduce(self.current_room)

    def collide_x(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        ogre_hit_list = []
        hut_hit_list = []
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[Ogre], False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, each.entity_list[hut.Hut], False)
            hut_hit_list = hut_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list, hut_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_x > 0 and item != self:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and item != self:
                    self.rect.left = item.rect.right

    def collide_y(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.entity_list[wall.Wall], False)
        ogre_hit_list = []
        hut_hit_list = []
        for each in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, each.entity_list[Ogre], False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
            neighbor_hit_list = pygame.sprite.spritecollide(self, each.entity_list[hut.Hut], False)
            hut_hit_list = hut_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list, hut_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_y > 0 and item != self:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and item != self:
                    self.rect.top = item.rect.bottom

    def find_home(self):
        possible_homes = []
        for possible_home in self.current_room.entity_list[hut.Hut]:
            home_dist = utilities.distance(possible_home.rect.x, possible_home.rect.y, self.rect.x, self.rect.y)
            possible_homes.append((home_dist, possible_home))
        possible_homes = sorted(possible_homes)
        self.home_hut = possible_homes[0][1]

    def idle(self):
        def go_home(self, home_x, home_y):

            home_dist = utilities.distance((home_x + 20), (home_y + 15), self.rect.x, self.rect.y)
            if home_dist > 100:
                changes = utilities.get_vector(self, self.home_hut.rect.x + 20, self.home_hut.rect.y + 15, self.rect.x + 10, self.rect.y + 10)
                self.change_x = changes[0]
                self.change_y = changes[1]
            else:
                self.change_y = 0
                self.change_x = 0
        if self.home_hut:
            go_home(self, self.home_hut.rect.x, self.home_hut.rect.y)
        else:
            pass

    def chase(self, current_room):
        if self.target_goblin is None or \
           self.target_goblin not in current_room.entity_list[goblin.Goblin]:
            self.target_goblin = self.pick_target(self.neighbors)

        changes = utilities.get_vector(self, self.target_goblin.rect.x + 7, self.target_goblin.rect.y + 7, self.rect.x + 10, self.rect.y + 10)
        self.change_x = changes[0]
        self.change_y = changes[1]
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
