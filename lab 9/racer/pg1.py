import pygame
import random
import time
from itertools import chain

pygame.init()

black = pygame.Color((0,0,0))
white = pygame.Color((255,255,255))
red = pygame.Color((255,0,0))
blue = pygame.Color((0,0,255))
green = pygame.Color((0,255,0))

screen_width = 400
screen_height = 600
speed = 5
score = 0
coin_score = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

background = pygame.image.load("AnimatedStreet.png")

screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(white)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
loop = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), -20)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, screen_width - 40), -20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < screen_width and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.weight = random.randint(1, 3)
        coord_range = list(chain(range(22, enemy.rect.center[0] - 24 - 22), range(enemy.rect.center[0] + 24 + 22, screen_width - 22)))
        self.rect.center = (random.choice(coord_range), 0)

    def move(self, enemy):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.rect.top = 0
            coord_range = list(chain(range(22, enemy.rect.center[0] - 24 - 22), range(enemy.rect.center[0] + 24 + 22, screen_width - 22)))
            self.rect.center = (random.choice(coord_range), 0)
            self.weight = random.randint(1, 3)

P1 = Player()
E1 = Enemy()
coin = Coin(E1)

enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(coin)

car_sprites = pygame.sprite.Group()
car_sprites.add(P1, E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, coin)

inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

while loop:
    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 1
        if event.type == pygame.QUIT:
            loop = False

    screen.blit(background, (0, 0))
    scores = font_small.render(str(score), True, black)
    coin_scores = font_small.render(f"Coins: {coin_score}", True, black)
    screen.blit(scores, (10, 10))
    screen.blit(coin_scores, (300, 10))

    for entity in car_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    screen.blit(coin.image, coin.rect)
    coin.move(E1)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1.5)
        screen.fill(red)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()

    if pygame.sprite.spritecollide(P1, coins_group, dokill=True):
        pygame.mixer.Sound("getcoin.mp3").play()
        coin_score += coin.weight
        coin = Coin(E1)
        coins_group.add(coin)
        all_sprites.add(coin)
        if coin_score % 5 == 0:
            speed += 1

    pygame.display.flip()
    clock.tick(60)