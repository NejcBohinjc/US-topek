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
font = pygame.font.SysFont("Arial", 32)

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
shoot_delay = 0.5
time_at_shoot = 0
coins = 0

#enemy nastavitve
time_at_enemy_spawn = 0
enemies_list = list()
time_at_enemy_spawn = 0
enemy_spawn_delay = 1.6
enemies_to_spawn = []
spawned_enemies = 0

#wave
wave_count = 0
wave_start_time = time.time()
enemy_count = 5
enemies_killed = 0
new_enemies_per_wave = 3
enemy_spawn_delay_deduction = 0.1
min_spawn_delay = 0.5


enemy_types = [
    {"class": enemy_script.Enemy, "sprite": "sprites/enemy_skull_sprite.png", "speed": 2.5, "damage": 5, "weight" : 7},
    {"class": enemy_script.Enemy_fast_weak, "sprite": "sprites/2_enemy_skull_sprite.png", "speed": 3.5, "damage": 2.5, "weight": 4},
    {"class": enemy_script.Enemy_slow_strong, "sprite": "sprites/enemy_slow_strong.png", "speed": 1, "damage": 8, "weight": 3}
]


#bullet
bullet_list = list()

#game states (gameplay,gameplay_pause,main_menu,game_over_menu,shop)
game_state = "main_menu"

#text settings
#game over menu text settings
game_over_text = font.render("Game Over!", True, (255, 255, 255))
game_over_text_x = 425
game_over_text_y = 135
#main menu text settings
main_menu_text = font.render("US topek", True, (255, 255, 255))
main_menu_text_x = 445
main_menu_text_y = 135
#shop text setting
coin_text_x = 10
coin_text_y = 10

shooting_delay_text = font.render("Faster shooting (5)", True, (255, 255, 255))
shooting_delay_text_x, shooting_delay_text_y = 100, 75
shooting_delay_button = Button.button(shooting_delay_text_x + 70, shooting_delay_text_y + 50,"sprites/buy_button.jpg",100,55)

#UI components
game_over_play_again_button = Button.button(425,190,"sprites/play_button.jpg",190,100)
main_menu_button = Button.button(425,300,"sprites/main_menu_button.jpg",190,100)
main_menu_play_button = Button.button(425,190,"sprites/play_button.jpg",190,100)
start_wave_button = Button.button(30,500,"sprites/start_wave_button.jpg",100,55)
shop_button = Button.button(30,425,"sprites/shop_button.jpg",100,55)
exit_shop_button = Button.button(10,530,"sprites/exit_button.jpg",100,55)

def reset_game():
    global time_at_enemy_spawn, enemy_count, wave_count, coins, shoot_delay
    top.health_points = top_health
    enemies_list.clear()
    enemy_count = 2
    top.bullets.clear()
    time_at_enemy_spawn = time.time()
    wave_count = 0
    coins = 0
    shoot_delay = 0.5
    new_wave()

def new_wave():
    global enemies_to_spawn, spawned_enemies, game_state, enemy_count, wave_count, enemies_killed, enemy_spawn_delay
    game_state = "gameplay"
    enemies_list.clear()
    enemies_to_spawn.clear()
    spawned_enemies = 0
    enemy_count += 3
    wave_count += 1
    enemies_killed = 0
    enemy_spawn_delay = max(min_spawn_delay, enemy_spawn_delay - enemy_spawn_delay_deduction)
    print(enemy_spawn_delay)

    print(f"this is wave {wave_count}")
    print(f"enemies to kill {enemy_count}")

    for _ in range(enemy_count):
        #k=1: vrni list z enim elementom, [0]: iz tega lista izberi prvi ele
        selected = random.choices(enemy_types, weights=[enemy["weight"] for enemy in enemy_types], k=1)[0]
        new_enemy = selected["class"](selected["sprite"], selected["speed"], selected["damage"], selected["weight"])
        enemies_to_spawn.append(new_enemy)


print(f"start of wave {wave_count}")
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == "gameplay":
        wave_text = font.render(f"Wave {wave_count}", True, (255, 255, 255))
        enemies_text = font.render(f"Enemies left: {enemy_count - enemies_killed}", True, (255, 255, 255))
        coin_text = font.render(f"Coins: {coins}", True, (255,255,255))
        
        #spawnanje enemy-ev
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            top.rotate("left",7)
        if keys[pygame.K_RIGHT]:
            top.rotate("right",7)
        
        if keys[pygame.K_SPACE]:
                if current_time - time_at_shoot > shoot_delay:
                    time_at_shoot = current_time
                    top.shoot()
        
        #spawnanje + setup enemy-ov
        if current_time - time_at_enemy_spawn > enemy_spawn_delay and game_state == "gameplay":
            time_at_enemy_spawn = current_time
            
            if spawned_enemies < len(enemies_to_spawn):
                new_enemy = enemies_to_spawn[spawned_enemies]
                enemies_list.append(new_enemy)
                spawned_enemies +=1
        
        if enemies_killed >= enemy_count and game_state == "gameplay":
            game_state = "gameplay_pause"
        
        #preveri collisione za vsakega enemy-a v listu , če collide-a s top-om
        for enemy in enemies_list[:]:
            if top.rect.colliderect(enemy.enemy_rect):
                #enemy destroy
                #print(f"destroy enemy {time.time()}")
                enemies_list.remove(enemy)
                enemies_killed += 1
                print(f'enemies eliminated {enemies_killed}')

                
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
                    enemies_killed += 1
                    coins += 1
                    print(f"coin c: {coins}")
                    print(f'enemies eliminated {enemies_killed}')

                    break 



        #top.draw(screen)
        screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
        screen.blit(barbed_wire,(width//2 - 60, height//2-45))
        screen.blit(wave_text, (350, 20))
        screen.blit(enemies_text, (480,20))
        screen.blit(coin_text, (coin_text_x,coin_text_y))
        if game_state == "gameplay_pause":
            start_called = start_wave_button.draw(screen)
            shop_called = shop_button.draw(screen)
            if start_called:
                print("start of wave called")
                print(f'{enemy_count} - {enemies_killed} = {enemy_count - enemies_killed}')
                new_wave()
                game_state = "gameplay"
            if shop_called:
                game_state = "shop"
        top.update_bullets()
        top.draw(screen)
        
        #spawnamo enemy-e
        for enemy in enemies_list:
            enemy.spawn(screen)
            enemy.update()
        
        """DEBUGGING
        pygame.draw.rect(screen, (255, 0, 0), top.rect, 2)
        for enemy in enemies_list:
            pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect, 2)
        
        pygame.draw.circle(screen,"#ffffff",(config.player_x,config.player_y),5) #narišemo center topa za testiranje
        """
    
    if game_state == "shop":
        screen.fill(background_colour)
        coin_text = font.render(f"Coins: {coins}", True, (255,255,255))
        screen.blit(coin_text, (coin_text_x,coin_text_y))
        screen.blit(shooting_delay_text, (shooting_delay_text_x,shooting_delay_text_y))
        
        shoot_dela_b = shooting_delay_button.draw(screen)
        if shoot_dela_b and coins >= 5:
            coins -=5
            shoot_delay = max(0.1, shoot_delay - 0.15)
            print(f"shoot delay = {shoot_delay}")
        
        exit_shop_b = exit_shop_button.draw(screen)
        if exit_shop_b:
            game_state = "gameplay_pause"
    
    if game_state == "game_over_menu":
        screen.fill(background_colour)
        screen.blit(game_over_text, (game_over_text_x,game_over_text_y))
        game_over_play_again_button.draw(screen)
        main_menu_button.draw(screen)

        #če je uporabnik kliknil na gumb i.e. če je vrnila funkcija True
        if game_over_play_again_button.draw(screen):
            game_state = "gameplay_pause"
            reset_game()
        
        if main_menu_button.draw(screen):
            reset_game()
            game_state = "main_menu"

    
    if game_state == "main_menu":
        screen.fill(background_colour)
        screen.blit(main_menu_text, (main_menu_text_x,main_menu_text_y))
        main_menu_play_button.draw(screen)

        #če je pritisnjen play na main menu
        if main_menu_play_button.draw(screen):
            game_state = "gameplay_pause"
            reset_game()


            

    
    
    pygame.display.flip()

    clock.tick(60)
