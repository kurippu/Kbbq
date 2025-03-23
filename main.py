import sys
import pygame
from pygame.examples.audiocapture import sound

import button
import smoke
from random import *
#import meat



pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)

pygame.display.set_caption("The Korean BBQ Experience")
# mari smells
# in-game sprite objects
beer = pygame.image.load('beercan.png').convert_alpha()
grill = pygame.image.load('grill.webp').convert_alpha()
meat_images = [
    pygame.image.load('Meat.png').convert_alpha(),
    pygame.image.load('meat2.webp').convert_alpha(),
    pygame.image.load('almost_cooked_meat1.png').convert_alpha(),
    pygame.image.load('cooked_meat_1.png').convert_alpha(),
    pygame.image.load('burnt_meat_!.png').convert_alpha()
]

plate = pygame.image.load('plate.png').convert_alpha()
plate_2 = pygame.image.load('plate-2.png').convert_alpha()
hand = pygame.image.load('hand.webp').convert_alpha()
soju = pygame.image.load('glass.webp').convert_alpha()
rice_paper = pygame.image.load('rice_paper.png').convert_alpha()
meat_button = pygame.image.load('meat_button.png.png').convert_alpha()
hand2 = pygame.image.load("hand2.png").convert_alpha()
hand3 = pygame.image.load("hand2.png").convert_alpha()
pickle_plate = pygame.image.load('plate.png').convert_alpha()
pickles = pygame.image.load('pickles.png').convert_alpha()

# initialize meat array for summoning meat
meat_state = 0
meat1 = meat_images[meat_state]
#meats = pygame.sprite.Group()
#single_meat = meat.Meat(meats)

# in-game transformations (aka resizing our pngs)
hand = pygame.transform.scale(hand, (400, 400))
hand2 = pygame.transform.scale(hand2,(210,210))
hand3 = pygame.transform.scale(hand3,(210,210))
hand2 = pygame.transform.flip(hand2, False, True)
hand3 = pygame.transform.flip(hand3, True, True)

soju = pygame.transform.scale(soju, (200, 200))
rice_paper = pygame.transform.scale(rice_paper, (240,240))
pickles= pygame.transform.scale(pickles, (240,240))
meat1 = pygame.transform.scale(meat1, (240,240))
plate = pygame.transform.scale(plate, (320,320))
meat_button = pygame.transform.scale(meat_button, (240, 240))
pickle_plate = pygame.transform.scale(plate, (320,320))
pygame.display.set_icon(beer)

# load in main menu buttons
start_img = pygame.image.load('starting-image.webp').convert_alpha()
exiting_img = pygame.image.load('exiting-image.webp').convert_alpha()
title_img = pygame.image.load('titlescreen.webp').convert_alpha()
title_img = pygame.transform.scale(title_img, (1050, 80))

#load in game over menu buttons
gameover_img = pygame.image.load('gameover-title.png').convert_alpha()
again_img = pygame.image.load('Again_button.png').convert_alpha()


# pause/exit menu buttons images
resume_img = pygame.image.load('resume-image.webp').convert_alpha()
exit_mid_game_img = pygame.image.load('exit-image.webp').convert_alpha()
pause_img = pygame.image.load('Paused_menu_screen.webp').convert_alpha()
again_img=pygame.transform.scale(again_img, (exit_mid_game_img.get_width(), exit_mid_game_img.get_height()))

# make the button instances
start_button = button.Button(100, 300, start_img, 0.8)
exit_button = button.Button(700, 300, exiting_img, 0.8)
# make the pause/exit button instances
resume_button = button.Button(100, 300, resume_img, 0.8)
exit_mid_game_button = button.Button(700, 300, exit_mid_game_img, 0.8)
#make the again button instance
again_button = button.Button(100, 300, again_img, 0.8)

smoke_group = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()
delta_time = 0.1

# Timer that is counting down
counter, text = 60, '60'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

player_x = 1080 / 4
player_y = 400

meat_x = 50
meat_y = 50

plate_x = meat_x - 85
plate_y = meat_y - 60

dragging = False

# Sound effects
ouch_sound = pygame.mixer.Sound("ouch.mp3")
ouch_sound.set_volume(1.0)

sizzling_sound = pygame.mixer.Sound("sizzling.mp3")
sizzling_sound.set_volume(1.0)

# channel to make sure one sound effect is playing at a time
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1) # tried using this for sizzling (unsuccessful)

# sound playing boolean
sound_playing = False
sound_playing_2 = False

# Track how long the meat is being cooked
cooking_time = 0

# Track how long the meat is being cooked
cooking_time = 0

def player(x, y):
    screen.blit(hand, (x, y))

def draw_plate(x, y):
    screen.blit(plate, (x, y))

def draw_meat(x, y):
    screen.blit(meat1, (x, y))
    # screen.blit(meat_2,(0, 0))

# def spawn_meat():
#     new_meat = meat.Meat(meats)
#     meats.add(new_meat)

def main_menu():
    screen.fill((205, 205, 253))

    pygame.mixer.music.load('wave-of-you-relaxing-lofi-305565.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)

    screen.blit(title_img, (110, 200))
    run = True
    while run:
        if start_button.draw(screen):
            pygame.mixer.music.stop()
            game_loop()
        if exit_button.draw(screen):
            run = False

        # Event handler
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()


def mid_game_menu():
    screen.fill((185, 237, 255))
    screen.blit(pause_img, (330, 100))
    pygame.mouse.set_visible(True)

    pygame.mixer.music.pause()
    run = True
    while run:
        if resume_button.draw(screen):
            pygame.mixer.music.unpause()
            run = False
            
        elif exit_mid_game_button.draw(screen):
            pygame.quit()
            sys.exit()

        # Event handler
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()

def gameover_menu():
    global counter, text

    screen.fill((205, 205, 253))
    pygame.mouse.set_visible(True)

    pygame.mixer.music.load('wave-of-you-relaxing-lofi-305565.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)

    screen.blit(gameover_img, (110, 100))
    run = True
    while run:
        if again_button.draw(screen):
            pygame.mixer.music.stop()
            counter, text = 60, '60'.rjust(3)
            game_loop()
            
        elif exit_mid_game_button.draw(screen):
            pygame.quit()
            sys.exit()

        # Event handler
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()

def game_loop():
    global running, counter, text, meat_x, meat_y, \
    dragging, sound_playing, ouch_sound, cooking_time, \
    meat_state, meat1, single_meat, sound_playing_2

    pygame.mixer.music.load('KBBQ BG Music.mp3')
    pygame.mixer.music.play()

    while running:
        screen.fill((85, 52, 43))

        screen.blit(grill, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
        screen.blit(plate_2, (500, -50))
        draw_plate((SCREEN_WIDTH//1.5 )- 88,(SCREEN_HEIGHT//1.5) -65)
        screen.blit(pickles,((SCREEN_WIDTH//1.5),(SCREEN_HEIGHT//1.5)))
        screen.blit(soju, (900, 320))
        draw_plate(885, 40)
        screen.blit(rice_paper, (950, 100))
        screen.blit(meat_button, (100, 400))

        # Render the Time Remaining timer
        screen.blit(font.render(text, True, (255, 255, 255)), (32, 48))

        player_x, player_y = pygame.mouse.get_pos()

        if player_x >= SCREEN_WIDTH:
            player_x = SCREEN_WIDTH
        elif player_x == 0:
            player_x = 0
        if player_y >= SCREEN_HEIGHT:
            player_y = SCREEN_HEIGHT
        elif player_y == 0:
            player_y = 0

        draw_plate(plate_x, plate_y)
        draw_meat(meat_x, meat_y)
        #meats.draw(screen)

        player(player_x, player_y)
        screen.blit(hand2,(SCREEN_WIDTH//2+ SCREEN_WIDTH//7+15, 0))
        screen.blit(hand3,(SCREEN_WIDTH//2-SCREEN_WIDTH//5-35, 0))
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        meat_rect = meat1.get_rect(topleft=(meat_x + 100, meat_y + 100))
        meat_rect.width = meat1.get_width() // 2
        meat_rect.height = meat1.get_height() // 2

        grill_rect = grill.get_rect(center=(SCREEN_WIDTH / 2 + 95, SCREEN_HEIGHT // 2 + 230))
        grill_rect.width = grill.get_width() // 2
        grill_rect.height = grill.get_height() // 2
        hand_mask = pygame.mask.from_surface(hand)
        #pygame.draw.rect(screen, pygame.Color('red'), meat_rect) for debugging purposes
        meat_mask = pygame.mask.from_surface(meat)
        grill_mask = pygame.mask.from_surface(grill)
        #pygame.draw.rect(screen, pygame.Color('green'), grill_rect) for debugging purposes
        grill_mask.fill()
        plate_2rect = plate_2.get_rect(topleft=(600,0))
        plate_2rect.width = plate_2.get_width()//2
        plate_2rect.height = plate_2.get_height() //2
        pygame.draw.rect(screen, pygame.Color('red'), plate_2rect)
        pygame.mouse.set_visible(False)

        if meat_mask.overlap(hand_mask, (mouse_x - meat_rect.x, mouse_y - meat_rect.y)) \
                and pygame.mouse.get_pressed()[0]:
            dragging = True
            #single_meat.start_drag(mouse_x, mouse_y)
        else:
            #single_meat.stop_drag()
            dragging = False

        if grill_mask.overlap(hand_mask, (mouse_x - grill_rect.x, mouse_y - grill_rect.y)) \
                and not dragging and pygame.mouse.get_pressed()[0]:
            if not sound_playing:
                channel1.play(ouch_sound, loops=-1)
                sound_playing = True
        else:
            if sound_playing:
                channel1.stop()
                sound_playing = False

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1
                text = f'TIME REMAINING: {str(counter).rjust(3) if counter > 0 else gameover_menu()}'
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mid_game_menu()
            if event.type == pygame.MOUSEMOTION and dragging:
                meat_x, meat_y = mouse_x, mouse_y
                meat_rect.topleft = (meat_x, meat_y)

        if grill_rect.colliderect(meat_rect) and not dragging:  # for smoke on grill
            smoke_group.update()
            if not sound_playing_2:
                channel2.play(sizzling_sound, loops=-1)
                sound_playing_2 = True
            if len(smoke_group) < 100:
                pos = [meat_rect.centerx + randint(-10, 10), meat_rect.centery + randint(-10, 10)]
                angle = randint(-30, 30)
                direction = pygame.math.Vector2(0, -1).rotate(angle)
                speed = randint(2, 5)
                smoke.Smoke(smoke_group, pos, direction, speed)
            else:
                smoke_group.remove(smoke_group.sprites()[0])
            smoke_group.draw(screen)
        else:
            if sound_playing_2:
                channel2.stop()
                sound_playing_2 = False

            cooking_time += 1
        
        if cooking_time == 300:
            meat_state = 1
            meat1 = meat_images[meat_state]
        elif cooking_time == 600:
            meat_state = 2
            meat1 = meat_images[meat_state]
        elif cooking_time == 900:
            meat_state = 3
            meat1 = meat_images[meat_state]
        elif cooking_time == 1200:
            meat_state = 4
            meat1 = meat_images[meat_state]
        
        if plate_2rect.colliderect(meat_rect) and not dragging:
            if meat_state == 3:
                pass
            else:
                pass

        pygame.display.flip()
        clock.tick(60)

main_menu()

pygame.quit()
sys.exit()