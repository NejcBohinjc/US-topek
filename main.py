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
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #tukaj bo streljanje krogel
                pass

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        top.rotate("left")
        #print(top.angle)
    if keys[pygame.K_RIGHT]:
        top.rotate("right")
        #print(top.angle)

    screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
    top.draw(screen)
    pygame.display.flip()

    clock.tick(60)
