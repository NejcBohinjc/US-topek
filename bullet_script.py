import pygame
import math

class Bullet:
    def __init__(self,x,y,radius,color,speed,angle):
        self.x = x
        self.y = y
        self.radius = radius #polmer
        self.color = color
        self.speed = speed
        
        #tukaj usmerino bullet z upprabo kotnih funkcij, tukaj mi je pomagal ai, saj nisem ravno matematik :)
        self.vx = self.speed * math.cos(math.radians(angle))  # hitost za x
        self.vy = -self.speed * math.sin(math.radians(angle))  # hitrost za y (- je spredaj, ker pygame kordinati delujejo tako, da če greš dol se y poveča, ker je začetna pozicija levo zgoraj)

        #nastavimo rect
        self.rect = pygame.Rect(self.x - self.radius ,self.y - self.radius,self.radius * 2, self.radius * 2)
        
    
    def update(self):
        self.x += self.vx
        self.y += self.vy

        #updejtamo hitbox
        self.rect.x  = self.x - self.radius
        self.rect.y  = self.y - self.radius


    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius,0) #screen, barva, center, premer, debelina črte okrog

    def off_screen(self,width,height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height



