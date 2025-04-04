import pygame
import random
import config
import time
import math

class Enemy:
    def __init__(self,enemy_sprite, speed,damage):
        self.speed = speed
        self.damage = damage
        self.enemy_sprite = enemy_sprite
 
        #sprite
        self.image = pygame.image.load(enemy_sprite).convert_alpha()
        self.hitbox_width = self.image.get_width() // 2
        self.hitbox_height = self.image.get_height() // 2
        self.image = pygame.transform.scale(self.image, (self.hitbox_width, self.hitbox_height))


        #x,y sta random poziciji
        center_min_x = (config.screen_width // 2) - 250 #412
        center_max_x = (config.screen_width // 2) + 250 #812

        center_min_y = (config.screen_height // 2) - 50 #100 
        center_max_y = (config.screen_height // 2) + 50 #500
        self.x = -1
        self.y = -1

        while True:
            self.x = random.randint(self.hitbox_width, config.screen_width - self.hitbox_width)
            self.y = random.randint(self.hitbox_height, config.screen_height - self.hitbox_height)
            #print(f'{self.x}, {self.y}') #pokažemo spawn x,y za debugging
            
            if self.x < center_min_x or self.x > center_max_x:
                if self.y < center_min_y or self.y > center_max_y:
                    #print(f'{self.x}, {self.y}') #pokažemo spawn x,y za debugging
                    break  # If x is outside the restricted range, break out of the loop



        self.enemy_rect = pygame.Rect(self.x + (self.hitbox_width - self.hitbox_width // 3) // 2, 
                                      self.y + (self.hitbox_height - self.hitbox_height // 3) // 2,
                                      self.hitbox_width // 3,
                                      self.hitbox_height // 3) #dodamo enemy rect za collisione

    def spawn(self,screen):
        screen.blit(self.image, (self.x,self.y))

    
    def update(self):
        distance_x = config.player_x - 70 - self.x
        distance_y = config.player_y - 70 - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2) # pitagorov izrek za izračun razdalje enemy-a in playerja :)

        if distance != 0:
            self.x += (distance_x / distance) * self.speed
            self.y += (distance_y / distance) * self.speed
        
        self.enemy_rect.topleft = (self.x + (self.hitbox_width - self.enemy_rect.width) // 2, 
                                   self.y + (self.hitbox_height - self.enemy_rect.height) // 2)