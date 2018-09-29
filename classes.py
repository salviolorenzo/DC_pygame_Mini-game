import pygame
import sys
from random import randint
from time import sleep
import math

pygame.init()
#game window dimensions
screen_width = 800
screen_height = 800
#define game window
screen = pygame.display.set_mode((screen_width, screen_height))
#window name
game_name = pygame.display.set_caption('This Game')

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

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load('images/background.gif')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.height = 30
        self.width = 30
        self.image = pygame.Surface([self.width, self.height])
        self.image = ship_images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vel = 10
        self.lives = 3
        self.pickup_count = 0
        self.score = 0

    def move_left(self):
        self.image = ship_images[6]
        self.x -= self.vel
    def move_right(self):
        self.image = ship_images[2]
        self.x += self.vel
    def move_up(self):
        self.image = ship_images[0]
        self.y -= self.vel
    def move_down(self):
        self.image = ship_images[4]
        self.y += self.vel

    def update(self):
        #movements based on key presses
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and self.x < screen_width - self.width:
            self.move_right()
        if pressed[pygame.K_LEFT] and self.x > 0: 
            self.move_left()  
        if pressed[pygame.K_UP] and self.y > 0:
           self.move_up()
        if pressed[pygame.K_DOWN] and self.y < screen_height - self.height:
            self.move_down()

        self.rect.topleft = self.x, self.y

        #images with multiple key presses
        if pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT]:
            self.image = ship_images[3]
        elif pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]:
            self.image = ship_images[1]
        elif pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT]:
            self.image = ship_images[5]
        elif pressed[pygame.K_UP] and pressed[pygame.K_LEFT]:
            self.image = ship_images[7] 


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.width = 25
        self.height = 25
        self.image = pygame.Surface([self.width, self.height])
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.x = randint(0, screen_width-self.width)
        self.y = -30
        self.vel = 3
    
    def chase(self, player):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.x - player.x, self.y - player.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.x += -dx * self.vel
        self.y += -dy * self.vel  
        self.rect.topleft = self.x, self.y

class Pickup(pygame.sprite.Sprite):
    def __init__(self):
        super(Pickup, self).__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image = pizza_image
        self.rect = self.image.get_rect()
        self.x = randint(0, screen_width-self.width)
        self.y = randint(0, screen_height-self.height)
        self.rect.topleft = self.x, self.y
        
class Boost(Pickup):
    def __init__(self):
        super(Boost, self).__init__()
        self.width = 20
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
        self.rect = self.image.get_rect()
        self.x = randint(0, screen_width-self.width)
        self.y = randint(0, screen_height-self.height)
        self.rect.topleft = self.x, self.y   