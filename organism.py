import random
import math
import pygame
import colors
import utilities


class Organism(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.species = None

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def do_thing(self):
        raise NotImplementedError()

    def check_bound(self, current_room):
        if self.rect.left < 20:
            self.rect.left = 20
        if self.rect.right > 780:
            self.rect.right = 780
        if self.rect.top < 20:
            self.rect.top = 20
        if self.rect.bottom > 580:
            self.rect.bottom = 580

    def move(self, current_room, current_chunk):

        block_hit_list = []
        goblin_hit_list = []
        ogre_hit_list = []
        neighbor_hit_list = []

        # X checks
        self.rect.x += self.change_x
        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, current_chunk.goblins_list, False)
            for chunk in self.neighbors:
                neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.goblins_list, False))
                goblin_hit_list = goblin_hit_list + neighbor_hit_list
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, current_chunk.ogres_list, False)
            for chunk in self.neighbors:
                neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.ogres_list, False))
                ogre_hit_list = ogre_hit_list + neighbor_hit_list

        hit_lists = (wall_hit_list, goblin_hit_list, ogre_hit_list)

        print(self.change_x)
        print(self.change_y)

        for hit_list in hit_lists:


            for item in hit_list:

                if self.change_x > 0 and self.rect.right != item.rect.right:
                    self.rect.right = item.rect.left
                elif self.change_x < 0 and self.rect.left != item.rect.left:
                    self.rect.left = item.rect.right
            # places creature back inside play area if it bugs out
        self.check_bound(current_room)

        current_chunk = self.current_chunk
        chunk = current_chunk
        if self.rect.left < chunk.left:
            utilities.remove_from_chunk(self, self.species, self.current_chunk)
            utilities.place_in_chunk(self, current_room)
        if self.rect.right > chunk.right:
            utilities.remove_from_chunk(self, self.species, self.current_chunk)
            utilities.place_in_chunk(self, current_room)

        # Y checks
        self.rect.y += self.change_y

        wall_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, current_chunk.goblins_list, False)
            for chunk in self.neighbors:
                neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.goblins_list, False))
                goblin_hit_list = goblin_hit_list + neighbor_hit_list
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, current_chunk.ogres_list, False)
            for chunk in self.neighbors:
                neighbor_hit_list = (pygame.sprite.spritecollide(self, chunk.ogres_list, False))
                ogre_hit_list = ogre_hit_list + neighbor_hit_list

        hit_lists = (wall_hit_list, goblin_hit_list, ogre_hit_list)
        for hit_list in hit_lists:

            for item in hit_list:
                if self.change_y > 0 and self.rect.top != item.rect.top:
                    self.rect.bottom = item.rect.top
                elif self.change_y < 0 and self.rect.bottom != item.rect.bottom:
                    self.rect.top = item.rect.bottom
        self.check_bound(current_room)

        chunk = self.current_chunk
        if self.rect.top < chunk.top:
            utilities.remove_from_chunk(self, self.species, self.current_chunk)
            utilities.place_in_chunk(self, current_room)
        if self.rect.bottom > chunk.bottom:
            utilities.remove_from_chunk(self, self.species, self.current_chunk)
            utilities.place_in_chunk(self, current_room)

    def expire(self):

        utilities.remove_from_chunk(self, self.species, self.current_chunk)

        if self.species == "Goblin":
            self.current_room.coins_on_death.append(self.lifetime_coins)
            self.current_room.death_ages.append(self.age)
            self.current_room.goblins.remove(self)
        elif self.species == "Ogre":
            self.current_room.goblins_eaten_on_death.append(self.lifetime_goblins_eaten)
            self.current_room.ogre_death_ages.append(self.age)
            self.current_room.ogres.remove(self)
        

    def pick_target(self, neighbors, current_chunk_row, current_chunk_column):
        target_object = None
        current_chunk = self.current_chunk

        def look_near_me(neighbors, current_chunk):
            possible_targets = []
            nearby_targets = []
            if current_chunk.coins_list:
                nearby_targets = current_chunk.coins_list
            else:
                for chunk in neighbors:
                    for target in chunk.coins_list:
                        nearby_targets.append(target)
            if nearby_targets:
                for target in nearby_targets:
                    dist = utilities.distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
                    possible_targets.append([dist, target])
            if possible_targets:
                possible_targets = sorted(possible_targets)
                target_object = possible_targets[0][1]
                return target_object

        target_object = look_near_me(neighbors, current_chunk)

        # too far away, just pick one at random
        if target_object is None:
            target_object = random.choice(list(self.current_room.coins_list))

        assert target_object is not None
        return target_object
