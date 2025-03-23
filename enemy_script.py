import pygame
import random
import config

class Enemy:
    def __init__(self,speed,damage):
        self.speed = speed
        self.damage = damage

        #x,y sta random poziciji
        self.x = random.randint(30,config.screen_width)
        self.y = random.randint(50,config.screen_height)

        
        #sprite
        self.image = pygame.image.load("enemy_skull_sprite.png").convert_alpha()

        #nastavimo hitbox na velikost sprite-a
        self.hitbox_width = self.image.get_width() // 2
        self.hitbox_height = self.image.get_height() // 2

        self.image = pygame.transform.scale(self.image, (self.hitbox_width, self.hitbox_height))
    
    def spawn(self,screen):
        screen.blit(self.image, (self.x,self.y))
        
