import pygame
from pygame.locals import *
from random import randint
pygame.init()

clock = pygame.time.Clock()
fps = 60


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 625

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sla')


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pygame.image.load('image/ship.png')
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_bullet = pygame.time.get_ticks()
        self.hp = 3

    def update(self):
        ship_speed = 8

        #movimentação
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= ship_speed   
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += ship_speed
        if key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= ship_speed
        if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += ship_speed

        if key[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= ship_speed   
        if key[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += ship_speed
        if key[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= ship_speed
        if key[pygame.K_s] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += ship_speed

        #tiro
        cooldown = 400
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_bullet > cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_bullet = time_now
        
        if self.hp <= 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  
        self.image = pygame.image.load('image/bullet_ship.png')
        self.image = pygame.transform.scale(self.image, (18, 18))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 12
        if self.rect.y < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, asteroid_group, True):
            self.kill()
        
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  
        self.image = pygame.image.load('image/asteroid.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = randint(1, SCREEN_WIDTH - self.rect.width)
        self.rect.y = randint(-200, 1)
        self.speed = randint (5, 10)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, ship_group, False):
            self.kill()
            player.hp -= 1

ship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()

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

#controle de spawn dos asteroides
last_asteroid = pygame.time.get_ticks()
asteroid_timer = 500

def spawn_asteroid():
    global last_asteroid
    timer = pygame.time.get_ticks()
    if timer - last_asteroid > asteroid_timer:
        asteroid_group.add(Asteroid())
        last_asteroid = timer

run = True
while run:

    clock.tick(fps)

    draw_bg()
    spawn_asteroid()


    player.update()
    bullet_group.update()
    asteroid_group.update()

    ship_group.draw(screen)
    bullet_group.draw(screen)
    asteroid_group.draw(screen)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  

    pygame.display.update()

pygame.quit()