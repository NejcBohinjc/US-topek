import pygame
import topek_script
import bullet_script
import time
import config
import enemy_script
import random
import Button

pygame.init()
clock = pygame.time.Clock()
running = True

#lastnosti displaya
width = config.screen_width
height = config.screen_height
background_colour = "#c4a354"

#nastavimo nastavitve displaya
pygame.display.set_caption('US topek')
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

#vsi objekti v igri
top_health = 10
top = topek_script.Top("#000000",100,50,top_health)
barbed_wire = pygame.image.load("sprites/barbed_wire.png").convert_alpha()
barbed_wire = pygame.transform.scale(barbed_wire, (150,110))

#nastavitve topa
shoot_cooldown = 0.25
time_at_shoot = 0

#enemy nastavitve
time_at_enemy_spawn = 0
enemies_list = list()
time_at_enemy_spawn = 0
enemy_spawn_delay = 1.5

enemy_types = [
    {"class": enemy_script.Enemy, "sprite": "sprites/enemy_skull_sprite.png", "speed": 2, "damage": 5, "weight" : 7},
    {"class": enemy_script.Enemy2, "sprite": "sprites/2_enemy_skull_sprite.png", "speed": 3.2, "damage": 3, "weight": 4},
    {"class": enemy_script.Enemy_slow_strong, "sprite": "sprites/enemy_slow_strong.png", "speed": 1, "damage": 8, "weight": 3}
    #en mejhen pa hiter, ka dela mal damage-a
]


#bullet
bullet_list = list()

#game states (gameplay,main_menu,game_over_menu)
game_state = "main_menu"

#text settings
font = pygame.font.SysFont("Arial", 32)
#game over menu text settings
game_over_text = font.render("Game Over!", True, (255, 255, 255))
game_over_text_x = 425
game_over_text_y = 135
#main menu text settings
main_menu_text = font.render("US topek", True, (255, 255, 255))
main_menu_text_x = 445
main_menu_text_y = 135

#UI components
game_over_play_again_button = Button.button(425,190,"sprites/play_button.jpg")
main_menu_button = Button.button(425,300,"sprites/main_menu_button.jpg")
main_menu_play_button = Button.button(425,190,"sprites/play_button.jpg")

def reset_game():
    global time_at_enemy_spawn
    top.health_points = top_health
    enemies_list.clear()
    top.bullets.clear()
    time_at_enemy_spawn = time.time()


while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == "gameplay":
        #spawnanje enemy-ev
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            top.rotate("left",7)
        if keys[pygame.K_RIGHT]:
            top.rotate("right",7)
        
        if keys[pygame.K_SPACE]:
                if current_time - time_at_shoot > shoot_cooldown:
                    time_at_shoot = current_time
                    top.shoot()
        
        #spawnanje + setup enemy-ov
        if current_time - time_at_enemy_spawn > enemy_spawn_delay:
            time_at_enemy_spawn = current_time
            
            #k=1: vrni list z enim elementom, [0]: iz tega lista izberi prvi ele
            selected = random.choices(enemy_types, weights=[enemy["weight"] for enemy in enemy_types], k=1)[0] 
            new_enemy = selected["class"](selected["sprite"], selected["speed"], selected["damage"], selected["weight"])

            #dodamo enemy-a na list
            enemies_list.append(new_enemy)
        
        #preveri collisione za vsakega enemy-a v listu , če collide-a s top-om
        for enemy in enemies_list[:]:
            if top.rect.colliderect(enemy.enemy_rect):
                #enemy destroy
                #print(f"destroy enemy {time.time()}")
                enemies_list.remove(enemy)
                
                #lower top hp
                top.health_points -= enemy.damage
                print(top.health_points)
                if top.health_points <= 0:
                    game_state = "game_over_menu"
        
        for bullet in top.bullets[:]:
            for enemy in enemies_list[:]:
                if bullet.rect.colliderect(enemy.enemy_rect):
                    #print("hit")
                    #dodaj da gre bullet lahko čez, če imaš nek upgrade
                    
                    top.bullets.remove(bullet)
                    enemies_list.remove(enemy)

                    break 



        #top.draw(screen)
        screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
        screen.blit(barbed_wire,(width//2 - 60, height//2-45))
        top.update_bullets()
        top.draw(screen)
        
        """DEBUGGING
        pygame.draw.rect(screen, (255, 0, 0), top.rect, 2)
        for enemy in enemies_list:
            pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect, 2)
        
        pygame.draw.circle(screen,"#ffffff",(config.player_x,config.player_y),5) #narišemo center topa za testiranje
        """
        
        
        #spawnamo enemy-e
        for enemy in enemies_list:
            enemy.spawn(screen)
            enemy.update()
    
    if game_state == "game_over_menu":
        screen.fill(background_colour)
        screen.blit(game_over_text, (game_over_text_x,game_over_text_y))
        game_over_play_again_button.draw(screen)
        main_menu_button.draw(screen)

        #če je uporabnik kliknil na gumb i.e. če je vrnila funkcija True
        if game_over_play_again_button.draw(screen):
            game_state = "gameplay"
            reset_game()
        
        if main_menu_button.draw(screen):
            reset_game()
            game_state = "main_menu"

    
    if game_state == "main_menu":
        screen.fill(background_colour)
        screen.blit(main_menu_text, (main_menu_text_x,main_menu_text_y))
        main_menu_play_button.draw(screen)

        if main_menu_play_button.draw(screen):
            game_state = "gameplay"
            reset_game()


            

    
    
    pygame.display.flip()

    clock.tick(60)
