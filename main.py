import sys
import pygame
import button
import smoke
from random import *

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

flags = pygame.SCALED | pygame.FULLSCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags, vsync=1)

pygame.display.set_caption("The Korean BBQ Experience")
#mari smells
# in-game sprite objects
beer = pygame.image.load('beercan.png').convert_alpha()
grill = pygame.image.load('grill.webp').convert_alpha()
meat = pygame.image.load('Meat.png').convert_alpha()
plate = pygame.image.load('plate.png').convert_alpha()
plate_2 = pygame.image.load('plate-2.png').convert_alpha()
meat_2 = pygame.image.load('meat2.webp').convert_alpha()
hand = pygame.image.load('hand.webp').convert_alpha()
soju = pygame.image.load('glass.webp').convert_alpha()
big_red_button = pygame.image.load('meat_button.png.png').convert_alpha()
#soju = pygame.image.load('').convert_alpha()
sound_play = False

#in-game transformations (aka resizing our pngs)
hand = pygame.transform.scale(hand, (400, 400))
soju = pygame.transform.scale(soju, (280,280))
big_red_button = pygame.transform.scale(big_red_button, (200, 200))

pygame.display.set_icon(beer)

#load in main menu buttons
start_img = pygame.image.load('starting-image.webp').convert_alpha()
exiting_img = pygame.image.load('exiting-image.webp').convert_alpha()
title_img = pygame.image.load('titlescreen.webp').convert_alpha()
title_img = pygame.transform.scale(title_img, (1050, 80))


#pause/exit menu buttons images
resume_img = pygame.image.load('resume-image.webp').convert_alpha()
exit_mid_game_img = pygame.image.load('exit-image.webp').convert_alpha()
pause_img = pygame.image.load('Paused_menu_screen.webp').convert_alpha()


#make the button instances
start_button = button.Button(100, 300, start_img, 0.8)
exit_button = button.Button(700, 300, exiting_img, 0.8)
#make the pause/exit button instances
resume_button = button.Button(100, 300, resume_img, 0.8)
exit_mid_game_button = button.Button(700, 300, exit_mid_game_img, 0.8)
order_meat_button = button.Button(100, 500, big_red_button, 0.8)

smoke_group = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()
delta_time = 0.1

# Timer that is counting down
counter, text = 60, '60'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

player_x = 1080/4
player_y = 400

meat_x = 50
meat_y = 50

plate_x = meat_x - 105
plate_y = meat_y - 70

dragging = False

ouch_sound = pygame.mixer.Sound("ouch.mp3")

channel = pygame.mixer.Channel(0)

sound_playing = False

def player(x, y):
    screen.blit(hand,(x ,y))
   # Offset hand image to appear above the cursor
    #offset_y = -150  # You can tweak this value as needed
    #screen.blit(hand, (x - hand.get_width() // 2, y + offset_y))


def draw_plate(x,y):
    screen.blit(plate,(x, y))

def draw_meat(x, y):
    screen.blit(meat, (x, y))
    #screen.blit(meat_2,(0, 0))

def order_meat(x,y):


    if order_meat_button.draw(screen):
        draw_meat(x,y)

def main_menu():
    screen.fill((205, 205, 253))

    pygame.mixer.music.load('wave-of-you-relaxing-lofi-305565.mp3')
    pygame.mixer.music.play()

    screen.blit(title_img, (110,200))
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

def game_loop():
    global running, counter, text, meat_x, meat_y, dragging, sound_playing, ouch_sound

    pygame.mixer.music.load('KBBQ BG Music.mp3')
    pygame.mixer.music.play()

    while running:
        screen.fill((85, 52, 43))

        screen.blit(grill, (SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4))
        screen.blit(plate_2, (500,-50))
        screen.blit(soju, (1000, 400))

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
        order_meat(meat_x, meat_y)

        player(player_x, player_y)
        mouse_x,mouse_y = pygame.mouse.get_pos()


        meat_rect = meat.get_rect(topleft=(meat_x, meat_y))
        grill_rect = grill.get_rect()
        soju_rect = soju.get_rect()
        hand_mask = pygame.mask.from_surface(hand)
        meat_mask = pygame.mask.from_surface(meat)
        grill_mask = pygame.mask.from_surface(grill)
        soju_mask = pygame.mask.from_surface(soju)
        grill_mask.fill()
        soju_mask.fill()
        pygame.mouse.set_visible(False)

        if meat_mask.overlap(hand_mask, (mouse_x - meat_rect.x, mouse_y - meat_rect.y))\
                and pygame.mouse.get_pressed()[0]:
            dragging = True
        else:
            dragging = False

        if grill_mask.overlap(hand_mask, (mouse_x - grill_rect.x, mouse_y - grill_rect.y))\
                and not dragging and pygame.mouse.get_pressed()[0]:
            #ouch_sound = pygame.mixer.Sound("ouch.mp3")
            #ouch_sound.play()
            pass
            
        if soju_mask.overlap(hand_mask, (mouse_x - soju_rect.x, mouse_y - soju_rect.y)) and pygame.mouse.get_pressed()[0]:
            ouch_sound = pygame.mixer.Sound("ouch.mp3")
            ouch_sound.play()
            if not sound_playing:
                channel.play(ouch_sound, loops=-1)
                sound_playing = True
        else:
            if sound_playing:
                channel.stop()
                sound_playing = False

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1
                text = f'TIME REMAINING: {str(counter).rjust(3) if counter > 0 else "TIME IS UP!"}'
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mid_game_menu()
            if event.type == pygame.MOUSEMOTION and dragging:
                meat_x, meat_y = mouse_x, mouse_y
                meat_rect.topleft = (meat_x, meat_y)

        if grill_mask.overlap(meat_mask, (meat_rect.centerx - grill_rect.centerx, meat_rect.centery - grill_rect.centery)) and not dragging: #for smoke on grill
            smoke_group.update()
            if len(smoke_group) < 100:
                pos = [meat_rect.centerx + randint(-10, 10), meat_rect.centery + randint(-10, 10)]
                angle = randint(-30,30)
                direction = pygame.math.Vector2(0, -1).rotate(angle)
                speed = randint(2, 5)
                smoke.Smoke(smoke_group, pos, direction, speed)
            else:
                smoke_group.remove(smoke_group.sprites()[0])
            smoke_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)
       
main_menu()

pygame.quit()
sys.exit()
