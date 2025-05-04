import pygame
import topek_script
import time
import config
import enemy_script
import random
import Button
import health_bar

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
top_start_damage = 1
top = topek_script.Top("#000000",100,50,top_health,top_start_damage)
barbed_wire = pygame.image.load("sprites/barbed_wire.png").convert_alpha()
barbed_wire = pygame.transform.scale(barbed_wire, (150,110))
h_bar = health_bar.HealthBar(top.health_points)

#inicializiramo nastavitve topa. Potem se nastavijo v reset_game funkciji
shoot_delay = 0
time_at_shoot = 0
coins = 0

#enemy nastavitve
time_at_enemy_spawn = 0
enemies_list = list()
enemy_spawn_delay = 1.6
enemies_to_spawn = [] #ta list napolnemo v new_wave funkciji z enemy-ji
spawned_enemies = 0

#wave
wave_count = 0
wave_start_time = time.time()
enemy_count = 0
enemies_killed = 0
new_enemies_per_wave = 3
enemy_spawn_delay_deduction = 0.1
min_spawn_delay = 0.8


enemy_types = [
    {"class": enemy_script.Enemy, "sprite": "sprites/enemy_skull_sprite.png", "speed": 1.4, "damage": 2.25, "weight" : 3, "health_points": 1},
    {"class": enemy_script.Enemy_fast_weak, "sprite": "sprites/2_enemy_skull_sprite.png", "speed": 1.8, "damage": 1.25, "weight": 4, "health_points": 1},
    {"class": enemy_script.Enemy_slow_strong, "sprite": "sprites/enemy_slow_strong.png", "speed": 1, "damage": 5, "weight": 3, "health_points": 2}
]

#game state (gameplay,gameplay_pause,main_menu,game_over_menu,shop)
game_state = "main_menu"

#text settings
#game over menu text settings
game_over_text = font.render("Game Over!", True, (255, 255, 255)) #pogooglal sem kako se rendera text, in kako se ga blita
game_over_text_x = 425
game_over_text_y = 135
#main menu text settings
main_menu_text = font.render("US topek", True, (255, 255, 255))
main_menu_text_x = 445
main_menu_text_y = 135
#shop text setting
coin_text_x = 10
coin_text_y = 10

#shop gumbi
shooting_delay_text = font.render("Faster shooting (5)", True, (255, 255, 255))
shooting_delay_text_x, shooting_delay_text_y = 100, 75
shooting_delay_button = Button.button(shooting_delay_text_x + 70, shooting_delay_text_y + 50,"sprites/buy_button.jpg",100,55)

damage_text = font.render("Damage (5)", True, (255, 255, 255))
damage_text_x, damage_text_y = 500, 75
damage_button = Button.button(damage_text_x + 15, damage_text_y + 50,"sprites/buy_button.jpg",100,55)

health_text = font.render("Reset Health (10)", True, (255, 255, 255))
health_text_x, health_text_y = 730, 75
health_button = Button.button(health_text_x + 65, health_text_y + 50,"sprites/buy_button.jpg",100,55)


#ostali gumbi
game_over_play_again_button = Button.button(425,190,"sprites/play_button.jpg",190,100)
main_menu_button = Button.button(425,300,"sprites/main_menu_button.jpg",190,100)
main_menu_play_button = Button.button(425,190,"sprites/play_button.jpg",190,100)
start_wave_button = Button.button(30,500,"sprites/start_wave_button.jpg",100,55)
shop_button = Button.button(30,425,"sprites/shop_button.jpg",100,55)
exit_shop_button = Button.button(900,530,"sprites/exit_button.jpg",100,55)

#izvši se ob vsakem začetku igre
def reset_game():
    global time_at_enemy_spawn, enemy_count, wave_count, coins, shoot_delay #vprašal sem chatgpt katere spremenljivke naj bodo globalne
    top.health_points = top_health
    enemies_list.clear()
    enemy_count = 2
    top.bullets.clear()
    time_at_enemy_spawn = time.time()
    wave_count = 0
    coins = 0
    shoot_delay = 0.5
    top.damage = 1
    new_wave()
    h_bar.reset() #resetiramo health topa (in s tem izgled health bar-a)

def new_wave():
    global enemies_to_spawn, spawned_enemies, game_state, enemy_count, wave_count, enemies_killed, enemy_spawn_delay
    game_state = "gameplay"
    enemies_list.clear()
    enemies_to_spawn.clear()
    spawned_enemies = 0
    enemy_count += new_enemies_per_wave
    wave_count += 1
    enemies_killed = 0
    enemy_spawn_delay = max(min_spawn_delay, enemy_spawn_delay - enemy_spawn_delay_deduction) #če gre delay slučajno pod minimalno vrednost delaya, izberemo max (kar je v tem primeru minimalni delay)
    #print(enemy_spawn_delay)

    #print(f"this is wave {wave_count}")
    #print(f"enemies to kill {enemy_count}")

    #tukaj generiramo list enemiov za vsak wave, ne spawnamo jih sproti. To idejo sem dobil sam, vendar sem uporabil AI da mi je to idejo pomagal spremeniti v kodo.
    for _ in range(enemy_count):
        selected = random.choices(enemy_types, weights=[enemy["weight"] for enemy in enemy_types], k=1)[0] #k=1: vrni list z enim elementom, [0]: iz tega lista izberi prvi ele
        #novega enemy-a v zogrnji vrstici izberemo z random choices na podlagi weights, ter new-enemy nastavimo na selected in vse njegove atribute nastavimo
        new_enemy = selected["class"](selected["sprite"], selected["speed"], selected["damage"], selected["weight"], selected["health_points"])
        enemies_to_spawn.append(new_enemy)


#print(f"start of wave {wave_count}")
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_state == "gameplay":
        wave_text = font.render(f"Wave {wave_count}", True, (255, 255, 255))
        enemies_text = font.render(f"Enemies left: {enemy_count - enemies_killed}", True, (255, 255, 255))
        coin_text = font.render(f"Coins: {coins}", True, (255,255,255))
        
        
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
        if current_time - time_at_enemy_spawn > enemy_spawn_delay:
            time_at_enemy_spawn = current_time
            
            if spawned_enemies < len(enemies_to_spawn):
                new_enemy = enemies_to_spawn[spawned_enemies]
                enemies_list.append(new_enemy)
                spawned_enemies +=1
        
        if enemies_killed >= enemy_count:
            game_state = "gameplay_pause"
        
        #preveri collisione za vsakega enemy-a v listu , če collide-a s top-om
        for enemy in enemies_list[:]:
            if top.rect.colliderect(enemy.enemy_rect):
                #enemy destroy
                #print(f"destroy enemy {time.time()}")
                enemies_list.remove(enemy)
                enemies_killed += 1
                h_bar.lower(enemy.damage)
                #print(f'enemies eliminated {enemies_killed}')

                
                #lower top hp
                top.health_points -= enemy.damage
                #print(top.health_points)
                if top.health_points <= 0:
                    game_state = "game_over_menu"
        
        #preverimo če bullet zadane enemy-a
        for bullet in top.bullets[:]:
            for enemy in enemies_list[:]:
                if bullet.rect.colliderect(enemy.enemy_rect):
                    
                    top.bullets.remove(bullet) #damo bullet stran iz lista
                    enemy.health_points -= top.damage
                    if enemy.health_points <= 0:
                        enemies_list.remove(enemy)
                        enemies_killed += 1
                        coins += 1
                        #print(f"coin c: {coins}")
                        #print(f'enemies eliminated {enemies_killed}')

                    break #če se zadane v enemy-a gremo ven, saj ne rabimo več preverjati collison-ov za ta bullet, ker se uniči



        #top.draw(screen)
        screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
        screen.blit(barbed_wire,(width//2 - 60, height//2-45))
        screen.blit(wave_text, (350, 20))
        screen.blit(enemies_text, (480,20))
        screen.blit(coin_text, (coin_text_x,coin_text_y))
        top.update_bullets()
        top.draw(screen)
        h_bar.update(screen)
        
        #spawnamo enemy-e
        for enemy in enemies_list:
            enemy.spawn(screen)
            enemy.update()
        
        """ DEBUGGING
        pygame.draw.rect(screen, (255, 0, 0), top.rect, 2)
        for enemy in enemies_list:
            pygame.draw.rect(screen, (0, 255, 0), enemy.enemy_rect, 2)
        
        pygame.draw.circle(screen,"#ffffff",(config.player_x,config.player_y),5) #narišemo center topa za testiranje
        """
    if game_state == "gameplay_pause":
        #print("this is gameplay_pause")
        wave_text = font.render(f"Wave {wave_count}", True, (255, 255, 255))
        enemies_text = font.render(f"Enemies left: {enemy_count - enemies_killed}", True, (255, 255, 255))
        coin_text = font.render(f"Coins: {coins}", True, (255,255,255))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            top.rotate("left",7)
        if keys[pygame.K_RIGHT]:
            top.rotate("right",7)

        if keys[pygame.K_SPACE]:
                if current_time - time_at_shoot > shoot_delay:
                    time_at_shoot = current_time
                    top.shoot()
        
        screen.fill(background_colour) #sproti nam riše ozadje in nam zato briše sled topa
        start_called = start_wave_button.draw(screen) #draw funkcija (v vsakem gumbu) nam vrne True če je bil gum pritisnjen
        shop_called = shop_button.draw(screen)



        if start_called:
            #print("start of wave called")
            #print(f'{enemy_count} - {enemies_killed} = {enemy_count - enemies_killed}')
            new_wave()
        if shop_called:
            game_state = "shop"
        
        screen.blit(wave_text, (350, 20))
        screen.blit(enemies_text, (480,20))
        screen.blit(barbed_wire,(width//2 - 60, height//2-45))
        screen.blit(coin_text, (coin_text_x,coin_text_y))
        top.update_bullets()
        h_bar.update(screen)
        top.draw(screen)
        


    if game_state == "shop":
        screen.fill(background_colour)
        coin_text = font.render(f"Coins: {coins}", True, (255,255,255))
        screen.blit(coin_text, (coin_text_x,coin_text_y))
        screen.blit(shooting_delay_text, (shooting_delay_text_x,shooting_delay_text_y))
        screen.blit(damage_text, (damage_text_x, damage_text_y))
        screen.blit(health_text, (health_text_x,health_text_y))
        
        if shoot_delay > 0.2:
            shoot_dela_b = shooting_delay_button.draw(screen)
        if shoot_dela_b and coins >= 5 and shoot_delay > 0.2:
            coins -=5
            shoot_delay = max(0.2, shoot_delay - 0.09) #tale max mi je ai predlagal in je kar dobra ideja, ker jaz sem hotel z if stavkom
            print(f"shoot delay = {shoot_delay}")
            time.sleep(0.3) #omogoči da player ne kupi več upgrade-ov naenkrat ponesreci
        
        if top.damage < 5:
            damage_b = damage_button.draw(screen)
        if damage_b and coins >= 5 and top.damage < 5:
            coins -= 5
            top.damage = min(5, top.damage + 0.5)
            print(f"top damage = {top.damage}")
            time.sleep(0.3)
        
        reset_health_b = health_button.draw(screen)
        if reset_health_b and coins >= 10:
            coins -= 10
            h_bar.reset()
            top.health_points = top_health
            print(f"top health = {top.health_points}")
            time.sleep(0.3)

        exit_shop_b = exit_shop_button.draw(screen)
        if exit_shop_b:
            game_state = "gameplay_pause"
            continue
    
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
