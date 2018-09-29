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
#colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 30
        self.height = 30 
        self.image = pygame.Surface((self.width,self.height))
        self.image = ship_images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vel = 7.5

        pygame.draw.rect(self.image, red, [self.x,self.y, 30,50])
    
        self.rect = self.image.get_rect()

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
    def __init__(self,direction, x, y):
        super(Enemy, self).__init__()
        self.width = 30
        self.height = 30
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((blue))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vel = 3
        self.direction = direction

        pygame.draw.rect(self.image, blue, [self.x,self.y, 30,30])

    def chase(self):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.x - hero.x, self.y - hero.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        # move along this normalized vector towards the player at current speed
        self.x += -dx * self.vel
        self.y += -dy * self.vel   
    

end = False
clock = pygame.time.Clock()
#generate player character
hero = Player(screen_width/2, screen_height*.45)

#generate enemies on all sides
enemy_left = Enemy('right', 0, randint(0,screen_height-30))
enemy_right = Enemy('left', screen_width-enemy_left.width, randint(0, screen_height- enemy_left.height))
enemy_top = Enemy('down', randint(0,screen_width-enemy_left.width), 0)
enemy_bottom = Enemy('up', randint(0,screen_width-enemy_left.width), screen_height-enemy_top.height)

#sprite groups
enemies = pygame.sprite.Group()
enemies.add(enemy_bottom, enemy_left, enemy_right, enemy_top)
all_sprites = pygame.sprite.Group()
all_sprites.add(hero, enemy_bottom, enemy_left, enemy_right, enemy_top)

#blit all sprites to screen
def blit_all():
    for character in all_sprites:
        screen.blit(character.image, (character.x, character.y))

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
            quit()
            
    
    screen.fill(black)
    enemy_bottom.chase()
    enemy_left.chase()
    enemy_right.chase()
    enemy_top.chase()
    hero.update()
    blit_all()

    pygame.display.update()
    clock.tick(60)