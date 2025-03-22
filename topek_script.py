import pygame
import math

class Top:
    def __init__(self,health,box_color,box_hitbox_width,box_hitbox_height,box_x,box_y,screen_width,screen_height):
        self.health = health
        self.box_color = box_color
        self.box_hitbox_width = box_hitbox_width
        self.box_hitbox_height = box_hitbox_height
        self.box_x = box_x
        self.box_y = box_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        #začetni kot nastavimo
        self.angle = 0

        self.original_image = pygame.image.load("BaseCannon.png").convert_alpha()

        self.box_hitbox_width = self.original_image.get_width()
        self.box_hitbox_height = self.original_image.get_height()

        
        #naredimo originalno, neobrnjeno sliko
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.box_x, self.box_y))




    def draw(self,screen):
        screen.blit(self.image, self.rect)

    def update_image(self):
        # Rotate the image
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        
        # Update position to keep it centered
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate(self,direction):
        rotation_speed = 2
        if direction == "left":
            self.angle -= rotation_speed
        elif direction == "right":
            self.angle += rotation_speed
        self.update_image()
        
    
    


        