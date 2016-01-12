import random
import math
import pygame
import colors
import entity
import utilities
import coin


class Organism(entity.Entity):

    def __init__(self, x, y, current_room, color, width, height):
        super().__init__(x, y, current_room, color, width, height)

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
        self.rect.x += self.change_x
        self.collide_x(current_room, current_chunk)
        self.check_bound(current_room)

        self.rect.y += self.change_y
        self.collide_y(current_room, current_chunk)
        self.check_bound(current_room)

        chunk = self.current_chunk
        if self.rect.top < chunk.top:
            self.current_chunk.entity_list[type(self)].remove(self)
            self.place_in_chunk(current_room)
        if self.rect.bottom > chunk.bottom:
            self.current_chunk.entity_list[type(self)].remove(self)
            self.place_in_chunk(current_room)
        if self.rect.left < chunk.left:
            self.current_chunk.entity_list[type(self)].remove(self)
            self.place_in_chunk(current_room)
        if self.rect.right > chunk.right:
            self.current_chunk.entity_list[type(self)].remove(self)
            self.place_in_chunk(current_room)


    def pick_target(self, neighbors, current_chunk_row, current_chunk_column):
        target_object = None
        current_chunk = self.current_chunk

        def look_near_me(neighbors, current_chunk):
            possible_targets = []
            nearby_targets = []
            nearby_targets = current_chunk.entity_list[self.food_type]
            for chunk in neighbors:
                for target in chunk.entity_list[self.food_type]:
                    nearby_targets.add(target)
            if nearby_targets:
                for target in nearby_targets:
                    dist = utilities.distance(target.rect.x, target.rect.y, self.rect.x, self.rect.y)
                    possible_targets.append((dist, target))
            if possible_targets:
                possible_targets = sorted(possible_targets)
                target_object = possible_targets[0][1]
                return target_object
            else:
                return None

        target_object = look_near_me(neighbors, current_chunk)

        # too far away, just pick one at random
        if target_object is None:
            target_object = random.choice(list(self.current_room.entity_list[self.food_type]))

        assert target_object is not None
        return target_object
