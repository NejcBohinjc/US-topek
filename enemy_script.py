import pygame
import random
import config
import time

class Enemy:
    def __init__(self,enemy_sprite, speed,damage):
        self.speed = speed
        self.damage = damage
        self.enemy_sprite = enemy_sprite


        
        #sprite
        self.image = pygame.image.load(enemy_sprite).convert_alpha()

        #nastavimo hitbox na velikost sprite-a
        self.hitbox_width = self.image.get_width() // 2
        self.hitbox_height = self.image.get_height() // 2

        self.image = pygame.transform.scale(self.image, (self.hitbox_width, self.hitbox_height))
    
        #x,y sta random poziciji
        self.x = random.randint(self.hitbox_width, config.screen_width - self.hitbox_width)
        self.y = random.randint(self.hitbox_height // 2,config.screen_height - self.hitbox_height)

    def spawn(self,screen):
        screen.blit(self.image, (self.x,self.y))
    
    def update(self):
        pass
    

         
        
