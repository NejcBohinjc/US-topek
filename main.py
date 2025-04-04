import pygame
import topek_script
import bullet_script
import time
import config
import enemy_script
import random

pygame.init()
clock = pygame.time.Clock()
#lastnosti displaya
width = config.screen_width
height = config.screen_height
background_colour = "#898a84"

#nastavimo nastavitve displaya
pygame.display.set_caption('US topek')
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

#vsi objekti v igri
top = topek_script.Top(100,"#000000",100,50)
#en1 = enemy_script.Enemy("enemy_skull_sprite.png",10,10)
running = True

#nastavitve topa
shoot_cooldown = 0.25
time_at_shoot = 0

#enemy nastavitve
time_at_enemy_spawn = 0
enemies_list = list()
time_at_enemy_spawn = 0
enemy_spawn_delay = 1.5

#bullet
bullet_list = list()

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
    
    #spawnanje enemy-ev
    if current_time - time_at_enemy_spawn > enemy_spawn_delay:
        time_at_enemy_spawn = current_time
        
        #generiramo random int, da nastavimo spawn chance
        spawn_chance = random.randint(0,10)

        if spawn_chance < 7:
            new_enemy = enemy_script.Enemy("sprites/enemy_skull_sprite.png",2,10)
        elif spawn_chance >= 7:
            new_enemy = enemy_script.Enemy2("sprites/2_enemy_skull_sprite.png",3.5,10)

        #ustvarimo nevega enemy-a
        #dodamo enemy-a na list 
        enemies_list.append(new_enemy)
    
    #preveri collisione za vsakega enemy-a v listu
    for enemy in enemies_list[:]:
        if top.rect.colliderect(enemy.enemy_rect):
            #enemy destroy
            #print(f"destroy enemy {time.time()}")
            enemies_list.remove(enemy)
            #lower top hp
    
    for bullet in top.bullets[:]:
        for enemy in enemies_list[:]:
            if bullet.rect.colliderect(enemy.enemy_rect):
                #print("hit")
                #dodaj da gre bullet lahko čez, če imaš nek upgrade
                
                top.bullets.remove(bullet)
                enemies_list.remove(enemy)

                break 

    """
    
    for bullet in top.bullets[:]:  # Use the `top.bullets` list
        bullet.update()
        if bullet.off_screen(width, height):
            top.bullets.remove(bullet)
        bullet.draw(screen)
    """




    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        top.rotate("left",7)
    if keys[pygame.K_RIGHT]:
        top.rotate("right",7)


    top.update_bullets()
    top.draw(screen)
    screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
    top.draw(screen)
    
    """DEBUGGING
    pygame.draw.rect(screen, (255, 0, 0), top.rect, 2)
    for enemy in enemies_list:
        pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect, 2)
    
    pygame.draw.circle(screen,"#ffffff",(config.player_x,config.player_y),5) #narišemo center topa za testiranje
    # """
    
    
    #spawnamo enemy-e
    for enemy in enemies_list:
        enemy.spawn(screen)
        enemy.update()
    

    pygame.display.flip()

    clock.tick(60)
