#!/usr/bin/python
import sys
import time

import spritesheet
import tiled_screen

import pygame

pygame.init()
pygame.mouse.set_visible(0)

TPS = 2 #Twitches per second, characters transitioning between different states
MPS = 3 #Movement per second, how many tiles the hero can walk per second

screen = tiled_screen.Screen(rows=9, columns=13, tile_width=64, tile_height=64)

chars_sheet = spritesheet.SpriteSheet("images/chars.png", background_color=(135, 191, 255, 255))
tiles_sheet = spritesheet.SpriteSheet("images/tiles.png", background_color=(0, 128, 128, 255))

hero = [chars_sheet.get_item(1, x, 64, 64, transparent=True) for x in range(8)]
screen.set_hero_down(hero[0:2])
screen.set_hero_right(hero[2:4])
screen.set_hero_left(hero[4:6])
screen.set_hero_up(hero[6:8])
screen.set_hero_tps(TPS)
screen.set_walking_speed(MPS)

brick_tile = tiles_sheet.get_item(0, 3, 64, 64)
screen.tile(brick_tile)

total_frames = 0

clock = pygame.time.Clock()
start = time.time()

pygame.mixer.init()
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.load('dw1castle.mid')
pygame.mixer.music.play(-1)

game_on = True
keys_down = set([])
while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
            continue

        if event.type == pygame.KEYUP:
            if event.dict['key'] == 27:
                #Escape
                game_on = False
                continue

        if event.type == pygame.KEYDOWN:
            key = event.dict['key']
            keys_down.add(key)
            if key == 273:
                #Up key
                #screen.walking_up()
                screen.walking_up()
            if key == 276:
                #Left
                screen.walking_left()
            if key == 274:
                #Down
                screen.walking_down()
            if key == 275:
                #Right
                screen.walking_right()

        if event.type == pygame.KEYUP:
            key = event.dict['key']
            if key in keys_down:
                keys_down.remove(key)

            if event.dict['key'] in (273, 274, 275, 276) and \
                    len(keys_down.intersection((273, 274, 275, 276))) == 0:
                #Any array key
                screen.stop_walking()

    screen.draw()
    clock.tick(tiled_screen.FPS)

end = time.time()
print 'Quitting...'
print 'Total Time = %.2f' % (end-start)
print 'Total Frames = %d' % (screen.total_frames)
print 'Average FPS = %.2f' % (screen.total_frames / (end-start))

pygame.quit()
