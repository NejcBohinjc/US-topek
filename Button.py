import pygame

class button:
    def __init__(self,x,y,image,scale_x,scale_y):
        #scale_x,scale_y = 190, 100
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale_x,scale_y)) #scale-amo sliko, da se prilega potrebam igre, scale_x in y podamo v parametrih, ko naredimo objekt Button
        self.rect = self.image.get_rect() #vzamemo dimenzije slike in rect nastavimo na te dimenzije
        self.rect.topleft = (x,y) #nastavimo zgornji kot (oz. pozicijo) gumba na paramera x in y, ki ju vnesemo ob tem ko naredimo objekt Button
    
    def draw(self, screen):
        #na yt sem pogledal kako bi naredil da preverim klik gumba
        clicked = False
        
        #dobimo pozicijo miške
        mouse_pos = pygame.mouse.get_pos()
        
        #preverimo če rect gumba collide-a z pozicijo miške
        if self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] == 1:
            clicked = True
            
        screen.blit(self.image, (self.rect.x,self.rect.y))
        return clicked