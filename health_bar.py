#tukaj mi je chatgpt malo pomagal, ker sta se mi bara narobo prikazovala
import pygame
import config

#deluje tako, da prikaže rediči bar ki je vedno isti, in nad njim še zeleni bar, ki se niža glede na to če te enemy zadane
class  HealthBar:
    def __init__(self,health):
        self.health = health
        self.bar_size = health
        self.y_offset = 75 #za koliko je bar zamaknjen nad igralcem
    
    def update(self, screen):
        #rdeči bar
        rect_red = pygame.Rect(config.player_x,config.player_y - self.y_offset,self.bar_size * 10, 30) #self.bar_size bo vedno zečetni health topa, ker nočemo da se to spremeni
        rect_red.center = (config.player_x,config.player_y - self.y_offset)
        pygame.draw.rect(screen, "#f24933", rect_red)
        
        #zeleni bar
        #vzame topleft[0] (x) in topleft[1] (y) od rdečega bara, da se naslika na isto pozicijo
        rect_green = pygame.Rect(rect_red.topleft[0], rect_red.topleft[1], self.health * 10, 30) #self.health, ker se krajša vedno ko te zadanejo
        pygame.draw.rect(screen, "#33f24c", rect_green)
    
    def lower(self, damage):
        self.health -= damage
    
    def reset(self):
        self.health = self.bar_size
