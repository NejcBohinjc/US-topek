import pygame
import topek_script
import bullet_script

pygame.init()
clock = pygame.time.Clock()
#lastnosti displaya
width = 1024
height = 600
background_colour = "#898a84"

#nastavimo nastavitve displaya
pygame.display.set_caption('US topek')
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

#vsi objekti v igri
top = topek_script.Top(100,"#000000",100,50,width/2,height/2,width,height)
bullet1 = bullet_script.Bullet(width/2,height/2,5,"#452563")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        top.rotate("left")
    if keys[pygame.K_RIGHT]:
        top.rotate("right")
    

    screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
    top.draw(screen)
    bullet1.draw(screen) #narišemo top + cev
    pygame.display.flip()

    clock.tick(60)
