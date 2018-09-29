import pygame
import sys
from random import randint
from time import sleep
import math
from classes import Player, Enemy, Pickup, Boost, Background

pygame.init()
pygame.font.init()
font_path = "extras/arcadeclassic.ttf"
font_size = 50
font_Obj = pygame.font.Font(font_path, font_size)
font_Obj2= pygame.font.Font(font_path, 30)

#game window dimensions
screen_width = 800
screen_height = 800
#define game window
screen = pygame.display.set_mode((screen_width, screen_height))
#window name
game_name = pygame.display.set_caption('Deep Space')

ship_images = [pygame.image.load('images/ship_up.png'), pygame.image.load('images/ship_up_right.png'), pygame.image.load('images/ship_right.png'), pygame.image.load('images/ship_down_right.png'), pygame.image.load('images/ship_down.png'), pygame.image.load('images/ship_down_left.png'), pygame.image.load('images/ship_left.png'), pygame.image.load('images/ship_up_left.png')]
ufo_image = pygame.image.load('images/ufo.png')
scaled_image = pygame.transform.scale(ufo_image, (30,30))
pizza_image = pygame.transform.scale(pygame.image.load('images/pizza.png'), (30,30))

#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

enemies = pygame.sprite.Group()
pickups = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
boost_group = pygame.sprite.Group() 

#enemy event
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 3000)
#pick up event
add_object = pygame.USEREVENT + 2
pygame.time.set_timer(add_object, 5000)
add_boost = pygame.USEREVENT + 3
pygame.time.set_timer(add_boost, 15000)


#blit all sprites to screen
def blit_all():
    for character in all_sprites:
        screen.blit(character.image, (character.x, character.y))

def opening_screen():
    begin = True
    while begin:
        screen.fill(white)
        welcome = font_Obj.render("DEEP     SPACE", 1, (black))
        screen.blit(welcome, (screen_width*.325, screen_height*.45))
        play = font_Obj2.render("PRESS  SPACE   TO  PLAY", 2, (black))
        screen.blit(play, (screen_width*.315, screen_height*.75))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    begin = False

def end_screen():
    end =True
    while end:
        pygame.mixer.music.pause()
        screen.fill(white)
        game_over = font_Obj.render("GAME   OVER", 1, (black))
        play = font_Obj2.render("PRESS  SPACE   TO  PLAY    AGAIN", 2, (black))
        end_game = font_Obj2.render("PRESS  X   TO  QUIT", 2, (black))
        score = hero.score
        game_score = font_Obj.render("SCORE    %d"%score, 2, (black))
        screen.blit(game_over,(screen_width*.345, screen_height*.35))
        screen.blit(play, (screen_width*.25, screen_height*.75))
        screen.blit(game_score, (screen_width*.375, screen_height*.50))
        screen.blit(end_game, (screen_width*.35, screen_height*.65))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end = False
                    game_loop()
                elif event.key == pygame.K_x:
                    pygame.quit()
            elif event.type == pygame.QUIT:
                pygame.quit()


def game_timer(time):
    seconds = time/1000
    timer = font_Obj2.render("Time  %d"%(seconds), 1, (white))
    screen.blit(timer, (10,0))
    pygame.display.update()

def display_lives(player):
    lives = player.lives
    display = font_Obj2.render("Lives  %d"%(lives), 1, (white))
    screen.blit(display, (screen_width-125,0))
    pygame.display.update()

def display_score(player):
    score = player.score
    display = font_Obj2.render("Score  %d"%(score), 1, (white))
    screen.blit(display, (screen_width-125,30))
    pygame.display.update()

def music():
    pygame.mixer.init()
    pygame.mixer.music.load('extras/soundtrack.mp3')
    pygame.mixer.music.play(-1)

hero = Player(screen_width*.475, screen_height*.7)
def game_loop():
    music()
    pygame.display.update()
    background = Background('images/background.gif', [0,0])
    end = False
    clock = pygame.time.Clock()
    #generate player character
    

    enemy_list = []
    hero_group.add(hero)
    all_sprites.add(hero)

    while not end:
        
        time = pygame.time.get_ticks()
        game_timer(time)
        display_score(hero)
        display_lives(hero)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                quit()

            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                enemy_list.append(new_enemy)
                all_sprites.add(new_enemy) 

            if event.type == add_object:
                new_pickup = Pickup()
                pickups.add(new_pickup)
                all_sprites.add(new_pickup)

            #if event.type == add_boost:
            #    boost = Boost()
            #    boost_group.add(boost)
            #    all_sprites.add(boost)

        if pygame.sprite.spritecollide(hero, enemies, False):
            hero.lives -= 1

        for enemy in enemy_list:
            if pygame.sprite.spritecollide(enemy, hero_group, False):
                enemy.kill()

        if pygame.sprite.spritecollide(hero, pickups, dokill = True):
            hero.pickup_count += 1
            hero.score += 1
            if hero.pickup_count == 5:
                hero.lives += 1
                hero.pickup_count = 0

        if hero.lives == 0:
            hero.kill()
            end = True

        screen.fill((white))
        screen.blit(background.image, background.rect)
        for enemy in enemy_list:
            enemy.chase(hero)
        hero.update()
        blit_all()

        pygame.display.update()
        clock.tick(60)

opening_screen()
game_loop()
end_screen()