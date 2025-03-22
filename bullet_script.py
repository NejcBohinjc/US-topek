import pygame

class Bullet:
    def __init__(self,x,y,radius,color,speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        
    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius,0)


