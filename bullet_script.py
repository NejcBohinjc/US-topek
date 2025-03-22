import pygame
import math

class Bullet:
    def __init__(self,x,y,radius,color,speed,angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed

        self.vx = self.speed * math.cos(math.radians(angle))  # X velocity
        self.vy = -self.speed * math.sin(math.radians(angle))  # Y velocity
    
    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius,0)

    def off_screen(self,width,height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height


