import pygame

class button:
    def __init__(self,x,y,image,scale_x,scale_y):
        #scale_x,scale_y = 190, 100
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale_x,scale_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self, screen):
        clicked = False
        #get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        
        #check if rect is colliding with mouse_pos
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            clicked = True
            
        screen.blit(self.image, (self.rect.x,self.rect.y))
        return clicked