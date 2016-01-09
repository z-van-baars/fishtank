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

    def move(self, current_room):

        block_hit_list = []
        goblin_hit_list = []
        ogre_hit_list = []
        # X checks
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, current_room.goblins, False)
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, current_room.ogres, False)

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

        block_hit_list = pygame.sprite.spritecollide(self, current_room.wall_list, False)
        if self.species == "Goblin":
            goblin_hit_list = pygame.sprite.spritecollide(self, current_room.goblins, False)
        if self.species == "Ogre":
            ogre_hit_list = pygame.sprite.spritecollide(self, current_room.ogres, False)

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

        chunk = current_room.chunk_rows[self.current_chunk_row][self.current_chunk_column]

        if self.rect.left < chunk.left:
            utilities.remove_from_chunk(self)
            utilities.place_in_chunk(self, current_room)
        if self.rect.right > chunk.right:
            utilities.remove_from_chunk(self)
            utilities.place_in_chunk(self, current_room)
        if self.rect.top < chunk.top:
            utilities.remove_from_chunk(self)
            utilities.place_in_chunk(self, current_room)
        if self.rect.bottom > chunk.bottom:
            utilities.remove_from_chunk(self)
            utilities.place_in_chunk(self, current_room)



    def pick_target(self, neighbors, current_chunk_row, current_chunk_column):
        target_object = None
        current_chunk = self.current_room.chunk_rows[current_chunk_row][current_chunk_column]

        def look_near_me(neighbors, current_chunk):
            possible_targets = []
            nearby_targets = []
            for chunk in neighbors:
                for target in chunk.coins_list:
                    nearby_targets.append(target)
            for target in nearby_targets:

                dist = utilities.distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
                possible_targets.append([dist, target])
            if possible_targets:
                possible_targets = sorted(possible_targets)
                target_object = possible_targets[0]
                return target_object
        look_near_me(neighbors, current_chunk)

        # too far away, just pick one at random
        if target_object is None:
            target_object = random.choice(list(self.current_room.coins_list))

        assert target_object is not None
        return target_object
