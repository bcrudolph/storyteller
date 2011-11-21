#!/usr/bin/python
import sys
import time

import pygame
import tiled_screen

pygame.init()
pygame.mouse.set_visible(0)

TPS = 2 #Twitches per second, characters transitioning between different states
MPS = 3 #Movement per second, how many tiles the hero can walk per second

screen = tiled_screen.Screen(rows=9, columns=13, tile_width=64, tile_height=64)

import maps.castle
import spritesheet
import zone

chars_sheet = spritesheet.SpriteSheet("images/chars.png", background_color=(135, 191, 255, 255))

hero = [chars_sheet.get_item(1, x, 64, 64, transparent=True) for x in range(8)]
screen.set_hero_down(hero[0:2])
screen.set_hero_right(hero[2:4])
screen.set_hero_left(hero[4:6])
screen.set_hero_up(hero[6:8])
screen.set_hero_tps(TPS)
screen.set_walking_speed(MPS)

pygame.mixer.init()
pygame.mixer.music.set_volume(0.8)

start_zone = maps.castle.Castle()
screen.set_zone(start_zone)

screen.update_grid()

total_frames = 0

clock = pygame.time.Clock()
start = time.time()

bump_sound = pygame.mixer.Sound('./sounds/bump.wav')
bump_sound.set_volume(0.8)
screen.set_bump_sound(bump_sound)

stair_sound = pygame.mixer.Sound('./sounds/stairs.wav')
stair_sound.set_volume(0.8)
screen.set_stair_sound(stair_sound)

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
                #spacebar
                screen.set_walking_speed(2.5*MPS)

        if event.type == pygame.KEYUP:
            key = event.dict['key']
            if key in keys_down:
                keys_down.remove(key)

            if key == 32:
                screen.set_walking_speed(MPS)

    if len(keys_down.intersection((273, 274, 275, 276))) == 0:
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
