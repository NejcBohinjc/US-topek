import pygame
import topek_script
import bullet_script
import time

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
running = True

#nastavitve topa
shoot_cooldown = 0.4
time_at_shoot = 0

while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #tukaj je streljanje krogel
                if current_time - time_at_shoot > shoot_cooldown:
                    time_at_shoot = current_time
                    top.shoot()



    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        top.rotate("left")
    if keys[pygame.K_RIGHT]:
        top.rotate("right")


    top.update_bullets()
    top.draw(screen)

    screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
    top.draw(screen)
    pygame.display.flip()

    clock.tick(60)
