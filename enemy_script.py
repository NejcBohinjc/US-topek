import pygame
import random
import config
import time
import math

#class za default enemy-a
class Enemy:
    def __init__(self,enemy_sprite,speed,damage,weight,health_points):
        self.speed = speed
        self.damage = damage
        self.enemy_sprite = enemy_sprite
        self.weight = weight
        self.health_points = health_points
 
        #sprite
        self.image = pygame.image.load(enemy_sprite).convert_alpha()
        self.hitbox_width = self.image.get_width() // 2
        self.hitbox_height = self.image.get_height() // 2
        self.image = pygame.transform.scale(self.image, (self.hitbox_width, self.hitbox_height))


        #x,y sta random poziciji
        #naredimo kot nekakšen navidezen box okrog topa, da se enemy-i ne spawnajo preblizu, kar pokvari uporabniško izkušnjo
        center_min_x = (config.screen_width // 2) - 350
        center_max_x = (config.screen_width // 2) + 350 

        center_min_y = (config.screen_height // 2) - 70
        center_max_y = (config.screen_height // 2) + 70
        
        #nastavimo x in y na nekaj, le za zečetek
        self.x = 0
        self.y = 0

        #tukaj sem uporabil AI, ker nisem vedel kako naj spawnam enemny-a le če je na določenem prostoru
        while True:
            self.x = random.randint(self.hitbox_width, config.screen_width - self.hitbox_width)
            self.y = random.randint(self.hitbox_height, config.screen_height - self.hitbox_height)
            #print(f'{self.x}, {self.y}') #pokažemo spawn x,y za debugging
            
            if self.x < center_min_x or self.x > center_max_x:
                if self.y < center_min_y or self.y > center_max_y:
                    #print(f'{self.x}, {self.y}') #pokažemo spawn x,y za debugging
                    break  # če je izven prepovedanega boxa, brake-aj izven loopa -> x in y sta nastavljena kot sta bila generirana
        

        #tukaj sem ai uporabil, da sem pravilno nastavil hitbox
        self.enemy_rect = pygame.Rect(self.x + (self.hitbox_width - self.hitbox_width // 3) // 2, 
                                      self.y + (self.hitbox_height - self.hitbox_height // 3) // 2,
                                      self.hitbox_width // 3,
                                      self.hitbox_height // 3) #dodamo enemy rect za collisione

    def spawn(self,screen):
        screen.blit(self.image, (self.x,self.y))

    
    def update(self):
        #tole mi je ai predlagal, ker nisem vedel kako naj naredim da grejo enmy-i proti centru
        #kodo sem prilagodil z drugimi imeni spremenljivk, -50 ter -25 kot primerno velikost playerja (50 je polovica x, 25 je polovica y playerja)
        distance_x = config.player_x - 50 - self.x
        distance_y = config.player_y - 25 - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2) # pitagorov izrek za izračun razdalje enemy-a in playerja

        if distance != 0:
            self.x += (distance_x / distance) * self.speed
            self.y += (distance_y / distance) * self.speed
        
        #premika hitbox enemy-a skupaj ko se premika enemy
        self.enemy_rect.topleft = (self.x + (self.hitbox_width - self.enemy_rect.width) // 2, 
                                   self.y + (self.hitbox_height - self.enemy_rect.height) // 2)
        

#podedujeta Enemy class

#2. enemy
#ai mi je pomagal spisai dedovanje za enemy-a
class Enemy_fast_weak(Enemy):
    def __init__(self, enemy_sprite, speed, damage,weight,health_points):
        super().__init__(enemy_sprite, speed, damage,weight,health_points)
    
    def spawn(self, screen):
        return super().spawn(screen)
    
    def update(self):
        return super().update()

#3. enemy
class Enemy_slow_strong(Enemy):
    def __init__(self, enemy_sprite, speed, damage, weight,health_points):
        super().__init__(enemy_sprite, speed, damage, weight,health_points)
    
    def spawn(self, screen):
        return super().spawn(screen)
    
    def update(self):
        return super().update()
    