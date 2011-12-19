#!/usr/bin/python
import sys
import time

import pygame

import chars
import menu
import sounds
import tiled_screen

if __name__ == '__main__':
    pygame.init()
    pygame.mouse.set_visible(0)

    screen = tiled_screen.Screen(rows=9, columns=13, tile_width=64, tile_height=64)

    import maps.castle
    start_zone = maps.castle.Castle()
    screen.set_zone(start_zone)

    screen.update_grid()

    clock = pygame.time.Clock()
    start = time.time()

    game_on = True

    pending_inputs = []
    keys_down = set([])
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                continue

            if 'key' not in event.dict:
                continue

            key = event.dict['key']
            if event.type == pygame.KEYDOWN and key == 27:
                #Escape
                game_on = False
                continue            

            if screen.game_state == tiled_screen.WORLD and \
                    event.type == pygame.KEYDOWN:

                keys_down.add(key)
                if key == 273:
                    #Up key
                    screen.walking_up()
                elif key == 276:
                    #Left
                    screen.walking_left()
                elif key == 274:
                    #Down
                    screen.walking_down()
                elif key == 275:
                    #Right
                    screen.walking_right()
                elif key == 32:
                    #Spacebar
                    screen.set_walking_speed(2.5*tiled_screen.MPS)
                elif key == 122:
                    #Z
                    if screen.motioning:
                        screen.stop_walking()
                        pygame.event.post(event)
                        continue

                    sounds.beep_sound.play()
                    screen.open_menu()
                    continue

	    if screen.game_state == tiled_screen.FIGHT and \
		    event.type == pygame.KEYDOWN:
		screen.zone.combat_manager.input(event)
		continue

            if event.type == pygame.KEYUP:
                if key in keys_down:
                    keys_down.remove(key)

                if key == 32:
                    screen.set_walking_speed(tiled_screen.MPS)

            if len(keys_down.intersection((273, 274, 275, 276))) == 0:
                #Any array key
                screen.stop_walking()

            if screen.game_state == tiled_screen.MENU and \
                    event.type == pygame.KEYDOWN:

                if key == 120:
                    #X
                    screen.close_menu()
                    screen.draw_world()
                elif key in (273, 274, 275, 276):
                    screen.menu[-1].move_selection(key, screen.total_frames)
                elif key == 122:
                    #Z
                    action = screen.menu[-1].selected()
                    if not action:
                        screen.draw()
                        clock.tick(tiled_screen.FPS)
                        continue

                    if action == 'close':
                        screen.close_menu()
                    elif action == 'close_all':
                        screen.close_all_menus()
                    elif action == 'talk':
                        row, col = screen.get_facing_square()

                        npc = screen.zone.get_npc_at(row, col)
                        dialogue = npc and npc.dialogue

                        if not dialogue:
                            tile_info = screen.zone.get_tile_info(row, col)
                            dialogue = tile_info.get('dialogue', [['There is no one here.']])

                        talk_menu = menu.TalkMenu(dialogue)
                        screen.open_menu(talk_menu)
                    else:
                        screen.open_menu(action)


        screen.draw()
        clock.tick(tiled_screen.FPS)

    end = time.time()
    print 'Quitting...'
    print 'Total Time = %.2f' % (end-start)
    print 'Total Frames = %d' % (screen.total_frames)
    print 'Average FPS = %.2f' % (screen.total_frames / (end-start))

    pygame.quit()
