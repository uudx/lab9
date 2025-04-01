#importing important libraries
from pygame.locals import *
import pygame
import random
import time
import sys

pygame.init()
clock = pygame.time.Clock()

#score count
global speed
count = 0
score = 0
speed = 1

#font
font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game over", True, (0,0,0))
score_font = font.render(f"Score: {score}", True, 60)
count_font = font.render(f"Earned coins: {count}", True, 60)

#path to folder with png images
path = r"C:\Users\ip-it\OneDrive\Desktop\2D Traffic Racer Assets"

#path to road image and screen 
road = pygame.image.load(path+r"\road.png")
w,h = road.get_size()
screen = pygame.display.set_mode((w, h))

#player image and its position
player = pygame.image.load(path + r"\player.png")
player_size = player.get_size()
player_pos = pygame.Vector2(w/2,h-player_size[1])
#Enemy logic
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load(path + "\enemy.png")
        self.enemy_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(0,w-self.enemy_size[0]),0)
 
      def move(self):
        global speed
        self.rect.move_ip(0,speed)
        if (self.rect.bottom > h+self.enemy_size[1]):
            self.rect.top = 0
            self.rect.center=(random.randint(0,w-self.enemy_size[0]),0)
 
      def draw(self, surface):
        surface.blit(self.image, self.rect)

#PLayer logic
class PLayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(path+"\player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (player_pos)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left>0 and pressed_keys[K_a]:
            self.rect.move_ip(-5,0)
        if self.rect.right<w and pressed_keys[K_d]:
            self.rect.move_ip(5,0)
        if self.rect.bottom<h and pressed_keys[K_s]:
            self.rect.move_ip(0,5)
        if self.rect.top>0 and pressed_keys[K_w]:
            self.rect.move_ip(0,-5)
    def draw(self, surface):
        surface.blit(self.image,self.rect)

#Coins
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def draw(self, surface, at_point, weight):
        self.image = pygame.image.load(path+f"\coin{weight}.png")
        self.rect = self.image.get_rect()
        self.image_size = self.image.get_size()
        self.rect.center = at_point
        surface.blit(self.image, self.rect)
        


coin = Coins()
P1 = PLayer()

#5 different enemies
enemy1 = Enemy()
enemy2 = Enemy()

#Creating groups
enemies = pygame.sprite.Group()
enemies.add(enemy1, enemy2,)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(enemy1,enemy2)

#generate weight of a coin
weight = random.choice([1,5,10])

#coordinates of the first coin
at_point = (random.randint(0,w-80), random.randint(0,h-80))
while True:
    #quiting
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #Backround(road)
    screen.blit(road, (0,0))
    
    #fonts of score and number of earned coins
    screen.blit(score_font, (w-400,200))
    screen.blit(count_font, (20,200))

    #drawing entity and moving
    for entity in all_sprites:
        entity.draw(screen)
        entity.move()
    
    #drawing a coin
    coin.draw(screen,at_point, weight)

    #cheking touch of player and coin and create another coin at random point
    if pygame.sprite.collide_rect(P1, coin):
        score += weight
        count += 1
        speed += .2
        weight = random.choice([1,5,10])
        at_point = (random.randint(0,w-80), random.randint(0,h-80))

    #updating the score
    score_font = font.render(f"Score: {score}", True, 60)
    count_font = font.render(f"Earned coins: {count}", True, 60)

    #chekning touch of player and enemies, ending
    if pygame.sprite.spritecollideany(P1, enemies):
          screen.fill((255,0,0))
          screen.blit(game_over, (w/3,h/2))
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()     
    
    #updating display
    pygame.display.update()

    #FPS limit
    clock.tick(60)
