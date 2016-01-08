import pygame
import utilities
import colors
import organism


class Ogre(organism.Organism):
    def __init__(self, x, y, speed):
        organism.Organism.__init__(self)
        self.image = pygame.Surface([20, 20])
        self.image.fill(colors.red)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target_goblin = None
        self.speed = speed
        self.goblins_eaten = 0
        self.lifetime_goblins_eaten = 0
        self.species = "Ogre"

    def do_thing(self, current_room):
        if self.target_goblin:
            self.chase(current_room)

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
        goblin_hit_list = []
        goblin_hit_list = pygame.sprite.spritecollide(self, current_room.goblins, True)
        for goblin in goblin_hit_list:
            current_room.goblins.remove(goblin)
            self.goblins_eaten += 1
            self.lifetime_goblins_eaten += 1
            self.ticks_without_food = 0
            current_room.deaths_by_ogre += 1
            current_room.coins_on_death.append(goblin.lifetime_coins)
            current_room.death_ages.append(goblin.age)

    def reproduce(self, current_room):
        self.goblins_eaten = 0
        new_ogre = Ogre((self.rect.x + 22), self.rect.y, self.speed)
        current_room.ogres.add(new_ogre)
