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

        if self.current_chunk:
            utilities.remove_from_chunk(self)
        utilities.place_in_chunk(self, current_room)

    def pick_target(self, possible_targets):
        target_object = None

        def look_within_cutoff(cutoff):
            for target in possible_targets:
                if abs(target.rect.x - self.rect.x) < cutoff and \
                   abs(target.rect.y - self.rect.y) < cutoff:
                    dist = utilities.distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
                    yield (dist, target)

        for cutoff in (8, 128):
            if possible_targets:
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
