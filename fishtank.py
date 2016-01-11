import pygame
import random
import math
import statistics
import organism
import goblin
import ogre
import utilities
import colors
import room

# To Do
# =====
# - Switch to vectors rather than X Y values


def graph_pop(screen, screen_height, time, current_room, goblin_pop_ticker, ogre_pop_ticker):
    goblin_pop = len(current_room.goblins)
    ogre_pop = len(current_room.ogres)
    goblin_pop = round(goblin_pop / 2)
    ogre_pop = round(ogre_pop)
    graph_time = round(time / 60)
    screen.blit(ogre_pop_ticker, [graph_time, ((screen_height - 1) - ogre_pop)])
    screen.blit(goblin_pop_ticker, [graph_time, ((screen_height - 1) - goblin_pop)])


def main():
    pygame.init()

    pygame.display.set_caption("There's always a bigger fish")

    screen_width = 800
    screen_height = 800
    screen = pygame.display.set_mode([screen_width, screen_height])
    tank_width = screen_width
    tank_height = screen_height - 200
    rooms = [room.Room1(tank_width, tank_height)]
    goblin_pop_log = []
    ogre_pop_log = []
    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()
    time = 0
    font = pygame.font.SysFont('Calibri', 18, True, False)
    goblin_pop_ticker = pygame.Surface([1, 1])
    goblin_pop_ticker.fill(colors.green)

    ogre_pop_ticker = pygame.Surface([1, 1])
    ogre_pop_ticker.fill(colors.red)

    tank_bg = pygame.Surface([tank_width, tank_height])
    tank_bg.fill(colors.black)

    done = False
    while not done:
        goblin_counter = font.render(str(len(current_room.entity_list[goblin.Goblin])), False, colors.black)
        starvation_counter = font.render(str(current_room.starvation_deaths), False, colors.red)
        old_age_counter = font.render(str(current_room.age_deaths), False, colors.red)
        ogre_counter = font.render(str(len(current_room.entity_list[ogre.Ogre])), False, colors.black)
        ogre_meals_counter = font.render(str(current_room.deaths_by_ogre), False, colors.black)
        goblin_pop_log.append(len(current_room.entity_list[goblin.Goblin]))
        ogre_pop_log.append(len(current_room.entity_list[ogre.Ogre]))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    coordin = utilities.spawn_org()
                    new_goblin = goblin.Goblin(coordin[0], coordin[1], current_room)
                    utilities.place_in_chunk(new_goblin, current_room)
                    current_room.entity_list[type(new_goblin)].add(new_goblin)
                    current_room.entity_list['movingsprites'].add(new_goblin)

                elif event.key == pygame.K_o:
                    coordin = utilities.spawn_org()
                    new_ogre = ogre.Ogre(coordin[0], coordin[1], current_room)
                    utilities.place_in_chunk(new_ogre, current_room)
                    new_ogre.pick_target(current_room)
                    current_room.entity_list[type(new_ogre)].add(new_ogre)
                    current_room.entity_list['movingsprites'].add(new_ogre)

                elif event.key == pygame.K_SPACE:
                    current_room.spawn_coins(100)

        current_room.update()
        graph_pop(screen, screen_height, screen_width, time, current_room, goblin_pop_ticker, ogre_pop_ticker)
        screen.blit(tank_bg, [0, 0])
        current_room.entity_list['movingsprites'].draw(screen)
        current_room.entity_list[room.Wall].draw(screen)
        current_room.entity_list[room.Coin].draw(screen)

        # debug function draws all goblins in every chunk
        # for row in range(len(current_room.chunk_rows)):
            # for item in range(len(current_room.chunk_rows[row])):
                # current_room.chunk_rows[row][item].goblins_list.draw(screen)

        screen.blit(goblin_counter, [1, 1])
        screen.blit(starvation_counter, [100, 1])
        screen.blit(old_age_counter, [200, 1])
        screen.blit(ogre_counter, [500, 1])
        screen.blit(ogre_meals_counter, [550, 1])
        pygame.display.flip()
        clock.tick(60)
        time += 1

    if current_room.death_ages:
        current_room.average_death_age = statistics.mean(current_room.death_ages)
    else:
        current_room.average_death_age = 0

    if current_room.coins_on_death:
        current_room.coins_on_death_average = statistics.mean(current_room.coins_on_death)
    else:
        current_room.coins_on_death_average = 0

    if current_room.ogre_death_ages:
        current_room.ogre_average_death_age = statistics.mean(current_room.ogre_death_ages)
    else:
        current_room.ogre_average_death_age = 0

    if current_room.goblins_eaten_on_death:
        current_room.ogre_average_goblins_eaten = statistics.mean(current_room.goblins_eaten_on_death)
    else:
        current_room.ogre_average_goblins_eaten = 0


    print("\n" * 5)
    print("Average age of Goblins at death: %s" % str(current_room.average_death_age))
    print("Average lifetime coins collected: %s" % str(current_room.coins_on_death_average))
    print("Starvation Deaths: %s" % str(current_room.starvation_deaths))
    print("Age Deaths: %s" % str(current_room.age_deaths))
    print("Deaths by Ogre: %s" % str(current_room.deaths_by_ogre))
    print("-")
    print("Average age of Ogres at death: %s" % str(current_room.ogre_average_death_age))
    print("Average number of Goblins eaten: %s" % str(current_room.ogre_average_goblins_eaten))
    pygame.quit()

if __name__ == "__main__":
    main()
