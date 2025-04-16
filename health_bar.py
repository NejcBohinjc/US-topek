#tukaj mi je chatgpt malo pomagal, ker sta se mi bara narobo prikazovale
import pygame
import config

class  HealthBar:
    def __init__(self,health):
        self.health = health
        self.size = health
        self.y_offset = 70
    
    def update(self, screen):
        #red bar
        rect_r = pygame.Rect(config.player_x,config.player_y - self.y_offset,self.size * 10, 30)
        rect_r.center = (config.player_x,config.player_y - self.y_offset)
        pygame.draw.rect(screen, "#f24933", rect_r)
        
        #green bar
        rect_g = pygame.Rect(rect_r.topleft[0], rect_r.topleft[1], self.health * 10, 30)
        pygame.draw.rect(screen, "#33f24c", rect_g)
    
    def lower(self, damage):
        self.health -= damage
