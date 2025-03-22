import pygame
import math
import bullet_script

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

        #nastavimo hitbox širino in višino na širino in višino ki jo ima slika
        self.box_hitbox_width = self.original_image.get_width()
        self.box_hitbox_height = self.original_image.get_height()

        
        #naredimo originalno, neobrnjeno sliko
        
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.box_x, self.box_y))

        self.bullets = list() #moramo narediti list, da se nam bulleti ne overwritajo




    def draw(self,screen):
        screen.blit(self.image, self.rect)

        #nariši vsak bullet iz lista
        for bullet in self.bullets:
            bullet.draw(screen)

    def update_image(self):
        # Rotate the image
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        
        # Update position to keep it centered
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def rotate(self,direction):
        rotation_speed = 2
                
        if direction == "left":
            self.angle += rotation_speed
        elif direction == "right":
            self.angle -= rotation_speed
            
        #kot gre lahko čez 360 stopinj, ali v minus, kar ni vredu, zato dodamo ta line
        self.angle %= 360

        self.update_image()

    def shoot(self):
        new_bullet = bullet_script.Bullet(self.rect.centerx, self.rect.centery, 5, "#ffffff", 10, self.angle)
        self.bullets.append(new_bullet)
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen(self.screen_width, self.screen_height):
                self.bullets.remove(bullet) 

        
    
    


        