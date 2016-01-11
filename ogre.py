import pygame
import utilities
import colors
import organism


class Ogre(organism.Organism):

    def __init__(self, x, y, current_room):
        super().__init__(self, x, y, current_room, colors.red, 20, 20)
        self.target_goblin = None
        self.speed = 3
        self.goblins_eaten = 0
        self.lifetime_goblins_eaten = 0
        self.change_x = 0
        self.change_y = 0
        self.age = 0
        self.ticks_without_food = 0

    def dead(self):
        if self.age > 2000:
            self.current_room.ogre_old_age_deaths += 1
            utilities.log("An ogre died of old age")
            self.current_room.goblins_eaten_on_death.append(self.lifetime_goblins_eaten)
            self.current_room.ogre_death_ages.append(self.age)
            self.expire()
            self.current_room.entity_list[movingsprites].remove(self)
            return True
        elif self.ticks_without_food > 300:
            self.current_room.ogre_starvation_deaths += 1
            utilities.log("An Ogre died of starvation")
            self.current_room.goblins_eaten_on_death.append(self.lifetime_goblins_eaten)
            self.current_room.ogre_death_ages.append(self.age)
            self.expire()
            self.current_room.entity_list[movingsprites].remove(self)
            return True

    def do_thing(self):
        self.age += 1
        self.ticks_without_food += 1

        if not self.dead():
            self.pick_target(self.current_room)
            if self.current_chunk_row is None or \
               self.current_chunk_column is None:
                utilities.place_in_chunk(self, self.current_room)
            if self.target_goblin:
                self.chase(self.current_room)
            self.move(self.current_room, self.current_chunk)
            if self.goblins_eaten > 39:
                self.reproduce(self.current_room)

    def collide_x(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        ogre_hit_list = pygame.sprite.spritecollide(self, current_chunk.ogres_list, False)
        for chunk in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.ogres_list, False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_x > 0 and item != self:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and item != self:
                    self.rect.left = item.rect.right
    def collide_y(self, current_room, current_chunk):
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        ogre_hit_list = pygame.sprite.spritecollide(self, current_chunk.ogres_list, False)
        for chunk in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.ogres_list, False))
            ogre_hit_list = ogre_hit_list + neighbor_hit_list
        hit_lists = (wall_hit_list, ogre_hit_list)

        for hit_list in hit_lists:
            for item in hit_list:
                if self.change_y > 0 and item != self:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and item != self:
                    self.rect.top = item.rect.bottom


    # overrides... but should it?
    def pick_target(self, current_room):
        goblin_distances = []
        target_goblin = []

        for goblin in current_room.goblins:
            dist = utilities.distance((goblin.rect.x + 7), (goblin.rect.y + 7), (self.rect.x + 10), (self.rect.y + 10))
            goblin_distances.append([dist, (goblin.rect.x, goblin.rect.y)])

        goblin_distances = sorted(goblin_distances)
        if goblin_distances:
            target_goblin = goblin_distances[0]
            target_goblin = target_goblin[1]
            self.target_goblin = target_goblin
        else:
            self.target_goblin = None
            self.change_x = 0
            self.change_y = 0

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
        goblin_hit_list = pygame.sprite.spritecollide(self, self.current_chunk.goblins_list, True)
        for chunk in self.neighbors:
            neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.goblins_list, True))
            goblin_hit_list = goblin_hit_list + neighbor_hit_list
        for goblin in goblin_hit_list:
            self.goblins_eaten += 1
            self.lifetime_goblins_eaten += 1
            self.ticks_without_food = 0
            current_room.deaths_by_ogre += 1
            current_room.coins_on_death.append(goblin.lifetime_coins)
            current_room.death_ages.append(goblin.age)
            current_room.goblins.remove(goblin)
            goblin.current_chunk.goblins_list.remove(goblin)
            current_room.movingsprites.remove(goblin)

    def reproduce(self, current_room):
        self.goblins_eaten = 0
        new_ogre = Ogre((self.rect.x + 22), self.rect.y, self.speed, current_room)
        new_ogre.check_bound(current_room)
        current_room.ogres.add(new_ogre)
        current_room.movingsprites.add(new_ogre)
