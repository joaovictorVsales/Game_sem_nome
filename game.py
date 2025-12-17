import pygame
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
fps = 60


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Invaders')


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pygame.image.load('image/ship.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_bullet = pygame.time.get_ticks()


    def update(self):
        speed_LR = 8
        speed_UD = 8

        #movimentação
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed_LR   
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed_LR
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed_UD
        if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += speed_UD

        #tiro
        cooldown = 400
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_bullet > cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_bullet = time_now
           

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pygame.image.load('image/bullet_ship.png')
        self.image = pygame.transform.scale(self.image, (18, 18))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 12
        

ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()

player = Ship(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 100)
ship_group.add(player)

bg = pygame.image.load('image/back.jpeg')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_img1 = 0
bg_img2 = -SCREEN_HEIGHT
bg_speed = 8


def draw_bg():
    global bg_img1, bg_img2

    bg_img1 += bg_speed
    bg_img2 += bg_speed

    if  bg_img1 >= SCREEN_HEIGHT:
        bg_img1 = bg_img2 - SCREEN_HEIGHT
    if  bg_img2 >= SCREEN_HEIGHT:
        bg_img2 = bg_img1 - SCREEN_HEIGHT
    

    screen.blit(bg, (0, bg_img1))
    screen.blit(bg, (0, bg_img2))


run = True
while run:

    clock.tick(fps)

    draw_bg()

    player.update()
    bullet_group.update()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  
   
    ship_group.draw(screen)
    bullet_group.draw(screen)
    
    pygame.display.update()

pygame.quit()
