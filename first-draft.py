import pygame

pygame.init()
#game window dimensions
screen_width = 800
screen_height = 800
#define game window
screen = pygame.display.set_mode((screen_width, screen_height))
#window name
game_name = pygame.display.set_caption('This Game')
#character dimensions
width = 50
height = 70
#starting positions-x/y
x = (screen_width/2) - width/2
y = screen_height*0.6
#character movement velocity
vel = 5

isJump = False
jumpCount = 10

end = False
clock = pygame.time.Clock()

while not end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_RIGHT] and x < screen_width - width:
        x += vel
    if pressed[pygame.K_LEFT] and x > 0:
        x -= vel
        
    if not isJump:    
        if pressed[pygame.K_UP] and y > 0:
           y -= vel
        if pressed[pygame.K_DOWN] and y < screen_height - height:
            y += vel
        if pressed[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10 
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(x,y,width,height))
    
    
    pygame.display.update()
    clock.tick(60)