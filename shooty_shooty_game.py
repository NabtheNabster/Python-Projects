import pygame
import math
import random
import json
try:
    with open("shooty_shooty_score.txt", "r") as f:
        scores = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    scores = []
pygame.init()
score = 0
#Title
Text = "Shooty Shooty Game"
displayed_letters = []
index = 0
letter_delay = 50
text_blink = 1000
text_flash = 0
last_update = pygame.time.get_ticks()
fps = 1000
highscore = float("inf")

# Window
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
screen_width = screen.get_width()
screen_height = screen.get_height()
pygame.display.set_caption("Shooter")
game_state = "game"
next_upgrade_score = 3
next_special_upgrade= 8
random_upgrades = [
    "lifesteal",
    "player speed",
    "bullet speed",
    "knockback",
    "fire rate"
]
random_spc_upgrades = [
    "fire bullets",
    "ricochet",
    "piercing bullets",
    "thorns",
    "extra shot"
]
fire_bullet = 0
ricochet = 0
piercing_bullet = 0
thorns = 0
extra_shot = 0
lifesteal = 0
knockback = 15
upgrade_picked = False
spc_upgrades = []
special_upgrades_chosen = False

#Sounds
gun_shot_sound = pygame.mixer.Sound("shot.wav")
enemy_hit_sound = pygame.mixer.Sound("enemy hit.wav")
enemy_death_sound = pygame.mixer.Sound("enemy_death.wav")
pygame.mixer.music.load("shooty_shooty_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
shoot_channel = pygame.mixer.Channel(0)
hit_channel = pygame.mixer.Channel(1)
enemy_death_channel = pygame.mixer.Channel(2)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 100)
game_over_font = pygame.font.Font(None, 150)

# Timers
last_hit_time = 0
damage_delay = 500
last_enemy_time = 0
last_shot_time = 0
enemy_hit_delay = 500
gun_shot_delay = 300
game_over_time = None
upgrade_shot_delay = 500
start_upgrade_time = 0

# Player
player_x = screen_width/2
player_y = screen_height/2
player_speed = 5.5 
player_size = 50
player_pos_old = True
player_health = 10
max_health = 10
p_color = (0,255,0)
hit_flash = 0
display_health = player_health
damage = 1

# Gun
gun_image = pygame.Surface((50, 20), pygame.SRCALPHA)
gun_image.fill((200, 200, 200))

# Bullets & Enemies
bullets = []
bullet_speed = 20
enemies = []
last_enemy_move = 0
enemy_move_delay = 16
death_effects = []
enemy_id_counter = 0

# Wall
wall_rect = pygame.Rect(325, 100, 0, 0)

def spawn_enemy():
    global enemy_id_counter
    side = random.choice(["top","bottom","left","right"])
    if side == "top":
        x, y = random.randint(0, screen_width), -50
    elif side == "bottom":
        x, y = random.randint(0, screen_width), screen_height + 50
    elif side == "left":
        x, y = -50, random.randint(0, screen_height)
    else:
        x, y = screen_width + 50, random.randint(0, screen_height)
    enemies.append([float(x), float(y), 5 + score//10, 0, 0, True, 5 + score//10, False, 0, enemy_id_counter, 1 + score//20])
    enemy_id_counter += 1
def exit_upgrade():
    global game_state, player_x, player_y, bullets, temp_extra_shot, extra_shot,done
    game_state = "game"
    player_x = old_player_x
    player_y = old_player_y
    extra_shot = temp_extra_shot
    done = False
    bullets.clear()
active_spc_upgrades = []
spawn_enemy()
running = True
state = "menu"
clock = pygame.time.Clock() # Added clock for consistent speed
current_random_upgrade = random.choice(random_upgrades)
done = False
while running:
    enemy_spawn_delay = max(500, 3000 - score * 50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if state == "menu" and event.key == pygame.K_SPACE:
                state = "game"
        if state == "game" or state == "menu":
            
            if player_health > 0 and event.type == pygame.MOUSEBUTTONDOWN and current_time - last_shot_time > gun_shot_delay:  
                dx = gun_x - player_rect.centerx
                dy = gun_y - player_rect.centery
                if dx != 0 or dy != 0:
                    # base angle of the mouse direction
                    base_angle = math.atan2(dy, dx)  # in radians

                    # spread between bullets in degrees
                    spread_deg = 10
                    total_bullets = extra_shot + 1  # always at least 1 bullet

                    # calculate starting angle so bullets are centered
                    start_angle = base_angle - math.radians(spread_deg * (total_bullets - 1) / 2)
                    if game_state == "special upgrade" or game_state == "upgrade":
                        if current_time - start_upgrade_time > upgrade_shot_delay:
                            for i in range(total_bullets):
                                angle = start_angle + math.radians(spread_deg * i)
                                new_dx = math.cos(angle)
                                new_dy = math.sin(angle)
                                bullets.append([gun_x, gun_y, new_dx, new_dy, 0, 0, set()])
                    else:
                        for i in range(total_bullets):
                            angle = start_angle + math.radians(spread_deg * i)
                            new_dx = math.cos(angle)
                            new_dy = math.sin(angle)
                            bullets.append([gun_x, gun_y, new_dx, new_dy, 0, 0, set()])
                last_shot_time = current_time
    current_time = pygame.time.get_ticks()
    if state == "menu":
        
        if index < len(Text) and current_time - last_update > letter_delay:
            displayed_letters.append(Text[index])
            index += 1
            last_update = current_time

        screen.fill((30,30,30))

        x = screen_width/2 - 300
        y = 100

        for char in displayed_letters:
            surf = title_font.render(char, True, (255,255,255))
            screen.blit(surf,(x,y))
            x += surf.get_width()
        if current_time - last_update > text_blink:
            text_flash += 50
            last_update = current_time
        if text_flash > 0:
            start_text = font.render("Press SPACE to start", True, (220,220,220))
            text_flash -= 1
        else:
            start_text = font.render("Press SPACE to start", True, (100,100,100))
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        screen.blit(start_text,(screen_width/2-120, 300))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(-(mouse_y - player_rect.centery), mouse_x - player_rect.centerx))
        rotated_gun = pygame.transform.rotate(gun_image, angle)
        gun_x = player_rect.centerx + math.cos(math.radians(angle)) * 30
        gun_y = player_rect.centery - math.sin(math.radians(angle)) * 30
        gun_rect = rotated_gun.get_rect(center=(gun_x, gun_y))
        for bullet in bullets[:]:
            bullet[0] += bullet[2] * bullet_speed
            bullet[1] += bullet[3] * bullet_speed
            if not (0 < bullet[0] < screen_width and 0 < bullet[1] < screen_height):
                bullets.remove(bullet)
            if pygame.Rect(bullet[0], bullet[1], 5, 5).colliderect(wall_rect) and game_state == "game":
                    hit_channel.play(enemy_hit_sound)
                    bullets.remove(bullet)
            if not (110 < bullet[0] < screen_width - 110 and 110 < bullet[1] < screen_height-110) and game_state == "upgrade":
                bullets.remove(bullet)
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
        for bullet in bullets:
            pygame.draw.circle(screen, (255,255,0), (int(bullet[0]), int(bullet[1])), 5)
            pygame.draw.circle(screen,(255,255,100), (int(bullet[0]), int(bullet[1])), 2)
        health_ratio = player_health / max_health
        player_hb = pygame.Rect(player_rect.x+4, player_rect.y+4, 42*health_ratio, 42)
        pygame.draw.rect(screen, (0,255,0), player_rect,4)
        pygame.draw.rect(screen, (0,255,0), player_hb)
        screen.blit(rotated_gun, gun_rect)
    elif state == "game":
        # --- PLAYER MOVEMENT WITH SLIDING ---
        keys = pygame.key.get_pressed()
        if player_health > 0 and game_state == "game":
            # Move X
            if keys[pygame.K_a]: player_x -= player_speed
            if keys[pygame.K_d]: player_x += player_speed
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            if player_rect.colliderect(wall_rect):
                if keys[pygame.K_d]: player_rect.right = wall_rect.left
                if keys[pygame.K_a]: player_rect.left = wall_rect.right
                player_x = player_rect.x

            # Move Y
            if keys[pygame.K_w]: player_y -= player_speed
            if keys[pygame.K_s]: player_y += player_speed
            player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
            if player_rect.colliderect(wall_rect):
                if keys[pygame.K_s]: player_rect.bottom = wall_rect.top
                if keys[pygame.K_w]: player_rect.top = wall_rect.bottom
                player_y = player_rect.y
        player_x = max(0, min(player_x, screen_width-player_size))
        player_y = max(0, min(player_y, screen_height-player_size))
        if game_state == "upgrade" and not upgrade_picked:
            current_random_upgrade = random.choice(random_upgrades)
            upgrade_picked = True 
        if game_state == "special upgrade" and not special_upgrades_chosen:
            spc_upgrades = random.sample(random_spc_upgrades, 3)
            special_upgrades_chosen = True
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        upgrade_rect = pygame.Rect(screen_width/2 - (screen_width-200)/2, screen_height/2 - (screen_height-200)/2, screen_width-200, screen_height-200)
        upgrade1_rect = pygame.Rect(166,screen_height/2-100,300,100)
        upgrade2_rect = pygame.Rect(532,screen_height/2-100,300,100)
        upgrade3_rect = pygame.Rect(898,screen_height/2-100,300,100)
        spc_upgrade1_rect = pygame.Rect(166,screen_height/2-100,300,100)
        spc_upgrade2_rect = pygame.Rect(532,screen_height/2-100,300,100)
        spc_upgrade3_rect = pygame.Rect(898,screen_height/2-100,300,100)
        # Gun rotation
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(-(mouse_y - player_rect.centery), mouse_x - player_rect.centerx))
        rotated_gun = pygame.transform.rotate(gun_image, angle)
        gun_x = player_rect.centerx + math.cos(math.radians(angle)) * 30
        gun_y = player_rect.centery - math.sin(math.radians(angle)) * 30
        gun_rect = rotated_gun.get_rect(center=(gun_x, gun_y))
        # Bullet logic
        for bullet in bullets[:]:
            bullet[0] += bullet[2] * bullet_speed
            bullet[1] += bullet[3] * bullet_speed
            if not (0 < bullet[0] < screen_width and 0 < bullet[1] < screen_height):
                bullets.remove(bullet)
            if pygame.Rect(bullet[0], bullet[1], 5, 5).colliderect(wall_rect) and game_state == "game":
                    hit_channel.play(enemy_hit_sound)
                    bullets.remove(bullet)
            if not (110 < bullet[0] < screen_width - 110 and 110 < bullet[1] < screen_height-110) and game_state == "upgrade":
                bullets.remove(bullet)
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            if game_state == "upgrade":
                if bullet_rect.colliderect(upgrade1_rect):
                    damage += 1
                    upgrade_picked = False
                    exit_upgrade()
                elif bullet_rect.colliderect(upgrade2_rect):
                    player_health += 2
                    max_health += 2
                    upgrade_picked = False
                    exit_upgrade()
                elif bullet_rect.colliderect(upgrade3_rect):

                    if current_random_upgrade == "lifesteal":
                        lifesteal += 0.4

                    elif current_random_upgrade == "player speed":
                        player_speed += 1

                    elif current_random_upgrade == "bullet speed":
                        bullet_speed += 2

                    elif current_random_upgrade == "knockback":
                        knockback += 3
                    elif current_random_upgrade == "fire rate":
                        gun_shot_delay -= 75
                    upgrade_picked = False
                    exit_upgrade()
            if game_state == "special upgrade":
                if bullet_rect.colliderect(spc_upgrade1_rect):
                    special_upgrades_chosen = False
                    active_spc_upgrades.append(spc_upgrades[0])
                    chosen = spc_upgrades[0]

                    if "fire bullets" in chosen:
                        fire_bullet += 1
                    elif "ricochet" in chosen:
                        ricochet += 1
                    elif "piercing bullets" in chosen:
                        piercing_bullet += 1
                    elif "thorns" in chosen:
                        thorns += 1
                    elif "extra shot" in chosen:
                        temp_extra_shot += 1
                    exit_upgrade()
                if bullet_rect.colliderect(spc_upgrade2_rect):
                    special_upgrades_chosen = False
                    active_spc_upgrades.append(spc_upgrades[1])
                    chosen = spc_upgrades[1]

                    if "fire bullets" in chosen:
                        fire_bullet += 1
                    elif "ricochet" in chosen:
                        ricochet += 1
                    elif "piercing bullets" in chosen:
                        piercing_bullet += 1
                    elif "thorns" in chosen:
                        thorns += 1
                    elif "extra shot" in chosen:
                        temp_extra_shot += 1

                    exit_upgrade()
                if bullet_rect.colliderect(spc_upgrade3_rect):
                    special_upgrades_chosen = False
                    active_spc_upgrades.append(spc_upgrades[2])
                    chosen = spc_upgrades[2]

                    if "fire bullets" in chosen:
                        fire_bullet += 1
                    elif "ricochet" in chosen:
                        ricochet += 1
                    elif "piercing bullets" in chosen:
                        piercing_bullet += 1
                    elif "thorns" in chosen:
                        thorns += 1
                    elif "extra shot" in chosen:
                        temp_extra_shot += 1
                    exit_upgrade()

        if current_time - last_enemy_time > enemy_spawn_delay and game_state == "game":
            spawn_enemy()
            last_enemy_time = current_time

        # --- ENEMY LOGIC WITH SLIDING ---
        if game_state == "game":
            for enemy in enemies[:]:
                enemy_speed = 1.2 + score * 0.01
                enemy_rect = pygame.Rect(int(enemy[0]), int(enemy[1]), 50, 50)

                # If touching the wall
                if enemy_rect.colliderect(wall_rect):

                    if enemy_rect.centery > wall_rect.centery:
                        enemy[1] += enemy_speed
                    elif enemy_rect.centery == wall_rect.centery:
                        enemy[1] += enemy_speed
                    else:
                        enemy[1] -= enemy_speed

                else:
                    # move toward player normally
                    if enemy[0] < player_x:
                        enemy[0] += enemy_speed
                    elif enemy[0] > player_x:
                        enemy[0] -= enemy_speed

                    if enemy[1] < player_y:
                        enemy[1] += enemy_speed
                    elif enemy[1] > player_y:
                        enemy[1] -= enemy_speed
                # Damage player
                if enemy_rect.colliderect(player_rect):
                    if current_time - last_hit_time > damage_delay:
                        player_health -= enemy[10]
                        if thorns >= 1:
                            enemy[2] -= damage/(2/thorns)
                        hit_flash = 10
                        last_hit_time = current_time
                # Bullet collision
                for bullet in bullets[:]:
                    bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)

                    if enemy_rect.colliderect(bullet_rect):

                        if enemy[9] not in bullet[6]:
                            bullet[6].add(enemy[9])
                            enemy[7] = True
                            if lifesteal > 0 :
                                player_health += lifesteal

                            enemy_hit_sound.set_volume(0.4)
                            hit_channel.play(enemy_hit_sound)

                            enemy[2] -= damage

                            # count total hits for piercing
                            bullet[5] += 1

                            # --- RICOCHET FIRST ---
                            if ricochet >= 1 and bullet[4] < ricochet:

                                dx_left = abs(bullet_rect.right - enemy_rect.left)
                                dx_right = abs(bullet_rect.left - enemy_rect.right)
                                dy_top = abs(bullet_rect.bottom - enemy_rect.top)
                                dy_bottom = abs(bullet_rect.top - enemy_rect.bottom)

                                min_overlap = min(dx_left, dx_right, dy_top, dy_bottom)

                                if min_overlap == dx_left or min_overlap == dx_right:
                                    bullet[2] *= -1  # flip X
                                else:
                                    bullet[3] *= -1  # flip Y

                                bullet[4] += 1

                            # --- PIERCE CHECK ---
                            elif bullet[5] > piercing_bullet:
                                if bullet in bullets:
                                    bullets.remove(bullet)
                                continue

                            # move bullet out of enemy to prevent sticking
                            bullet[0] += bullet[2]*1.3
                            bullet[1] += bullet[3]*1.3
                if enemy[2] <= 0:
                        death_effects.append([enemy_rect.centerx, enemy_rect.centery, 0, 40])
                        enemy_death_sound.set_volume(1)
                        enemy_death_channel.play(enemy_death_sound)
                        enemies.remove(enemy)
                        score += 1
                        break
                if fire_bullet >= 1 and enemy[7] == True:
                        if current_time- enemy[8] > enemy_hit_delay:
                            enemy[2] -= damage*(fire_bullet/3)
                            enemy[3] = 6
                            enemy[8] = current_time
                    
        if score  >= next_upgrade_score:
            start_upgrade_time = current_time
            game_state = "upgrade" 
            old_player_x = player_x
            old_player_y = player_y
            player_x = screen_width/2
            player_y = screen_height/2 + 225
            bullets.clear()
            next_upgrade_score =  3+round(next_upgrade_score*1.1)

        elif score >= next_special_upgrade:
            start_upgrade_time = current_time
            game_state = "special upgrade"
            old_player_x = player_x
            old_player_y = player_y
            player_x = screen_width/2
            player_y = screen_height/2 + 225
            bullets.clear()
            next_special_upgrade = 8+round(next_special_upgrade*1.1)
        if (game_state == "upgrade" or game_state == "special upgrade") and done == False:
            temp_extra_shot = extra_shot
            extra_shot = 0
            done = True
        # Drawing
        if display_health > player_health:
            display_health -= 0.1
        screen.fill((30,30,30))
        pygame.draw.rect(screen, (100,100,100), wall_rect)
        for effect in death_effects[:]:
                effect[2] += 2   # grow radius
                if effect[2] > effect[3]:
                    death_effects.remove(effect)
        for en in enemies:
            en_health_ratio = en[2]/en[6]
            en_rect = pygame.Rect(en[0], en[1], 50, 50)
            if en[3] > 0:
                pygame.draw.rect(screen, (255,255,255), en_rect,4)
                pygame.draw.rect(screen, (255,255,255), (en[0], en[1], 50*en_health_ratio, 46))
                en[3] -= 1
            else:
                pygame.draw.rect(screen, (200,0,0), en_rect,4)
                pygame.draw.rect(screen, (255,0,0), (en[0]+4, en[1]+4, 42*en_health_ratio, 42))
            for effect in death_effects:
                x, y, r, max_r = effect
                    
                # outer ring
                pygame.draw.circle(screen, (255,0,0), (int(x), int(y)), int(r), 3)
                
                # inner fill growing behind it
                inner_r = max(0, r)
                pygame.draw.circle(screen, (255,0,0), (int(x), int(y)), int(inner_r),4)
        if game_state == "upgrade" or game_state == "special upgrade":
            pygame.draw.rect(screen, (30,30,30), upgrade_rect)
            pygame.draw.rect(screen, (60,60,60), upgrade_rect, 10)
            if game_state == "upgrade":
                upgrade_text = font.render("UPGRADES", True, (255,255,255))
            else:
                upgrade_text = font.render("SPECIAL UPGRADES", True, (255,255,255))
            text_rect = upgrade_text.get_rect(center=(screen_width/2, 125))
            screen.blit(upgrade_text, text_rect)
            upgrade_text = font.render("Shoot the upgrade you wish to choose", True, (255,255,255))
            text_rect = upgrade_text.get_rect(center=(screen_width/2, 150))
            screen.blit(upgrade_text, text_rect)
            if game_state == "upgrade":
                pygame.draw.rect(screen, (30,30,30), upgrade1_rect)
                pygame.draw.rect(screen, (60,60,60), upgrade1_rect,5)
                pygame.draw.rect(screen, (30,30,30), upgrade2_rect)
                pygame.draw.rect(screen, (60,60,60), upgrade2_rect,5)
                pygame.draw.rect(screen, (30,30,30), upgrade3_rect)
                pygame.draw.rect(screen, (60,60,60), upgrade3_rect,5)
                dmg_text = font.render("Damage +1", True, (255,255,255))
                screen.blit(dmg_text, (upgrade1_rect.x + 80, upgrade1_rect.y + 40))
                hlt_text = font.render("Health +2", True, (255,255,255))
                screen.blit(hlt_text, (upgrade2_rect.x + 60, upgrade2_rect.y + 40))
                rdm_text = font.render(current_random_upgrade.upper(), True, (255,255,255))
                screen.blit(rdm_text, (upgrade3_rect.x + 50, upgrade3_rect.y + 40))
            else:
                pygame.draw.rect(screen, (173, 216, 230), spc_upgrade1_rect)
                pygame.draw.rect(screen, (0,0,255), spc_upgrade1_rect,5)
                pygame.draw.rect(screen, (144, 238, 144), spc_upgrade2_rect)
                pygame.draw.rect(screen, (0,255,0), spc_upgrade2_rect,5)
                pygame.draw.rect(screen, (255, 127, 127), spc_upgrade3_rect)
                pygame.draw.rect(screen, (255,0,0), spc_upgrade3_rect,5)
                if len(spc_upgrades) >= 3:
                    name = spc_upgrades[0]

                    if name == "fire bullets" and fire_bullet > 0:
                        display = f"{name} {fire_bullet+1}"
                    elif name == "ricochet" and ricochet > 0:
                        display = f"{name} {ricochet+1}"
                    elif name == "piercing bullets" and piercing_bullet > 0:
                        display = f"{name} {piercing_bullet+1}"
                    elif name == "thorns" and thorns > 0:
                        display = f"{name} {thorns+1}"
                    elif name == "extra shot" and temp_extra_shot > 0:
                        display = f"{name} {temp_extra_shot+1}"
                    else:
                        display = name
                    rdm_text = font.render(display.upper(), True, (255,255,255))
                    screen.blit(rdm_text, (spc_upgrade1_rect.x + 20, spc_upgrade1_rect.y + 40))
                    name = spc_upgrades[1]

                    if name == "fire bullets" and fire_bullet > 0:
                        display = f"{name} {fire_bullet+1}"
                    elif name == "ricochet" and ricochet > 0:
                        display = f"{name} {ricochet+1}"
                    elif name == "piercing bullets" and piercing_bullet > 0:
                        display = f"{name} {piercing_bullet+1}"
                    elif name == "thorns" and thorns > 0:
                        display = f"{name} {thorns+1}"
                    elif name == "extra shot" and temp_extra_shot > 0:
                        display = f"{name} {temp_extra_shot+1}"
                    else:
                        display = name
                    rdm_text = font.render(display.upper(), True, (255,255,255))
                    screen.blit(rdm_text, (spc_upgrade2_rect.x + 20, spc_upgrade2_rect.y + 40))
                    name = spc_upgrades[2]

                    if name == "fire bullets" and fire_bullet > 0:
                        display = f"{name} {fire_bullet+1}"
                    elif name == "ricochet" and ricochet > 0:
                        display = f"{name} {ricochet+1}"
                    elif name == "piercing bullets" and piercing_bullet > 0:
                        display = f"{name} {piercing_bullet+1}"
                    elif name == "thorns" and thorns > 0:
                        display = f"{name} {thorns+1}"
                    elif name == "extra shot" and temp_extra_shot > 0:
                        display = f"{name} {temp_extra_shot+1}"
                    else:
                        display = name
                    rdm_text = font.render(display.upper(), True, (255,255,255))
                    screen.blit(rdm_text, (spc_upgrade3_rect.x + 20, spc_upgrade3_rect.y + 40))
        for bullet in bullets:
            pygame.draw.circle(screen, (255,255,0), (int(bullet[0]), int(bullet[1])), 5)
            pygame.draw.circle(screen,(255,255,100), (int(bullet[0]), int(bullet[1])), 2)
        health_ratio = player_health / max_health
        if player_health > 0:
            if health_ratio > 1:
                player_health = max_health
            elif health_ratio > 0.75:
                po_color = (0,200,0)
                p_color = (0,255,0)
            elif health_ratio> 0.5:
                po_color = (200,200,0)
                p_color = (255,255,0)
            elif health_ratio> 0.25:
                po_color = (200,110,0)
                p_color = (255,165,0)
            elif health_ratio > 0:
                po_color = (200,0,0)
                p_color = (255,0,0)
            else:
                po_color = (200,0,200)
                p_color = (255,0,255)
            player_hb = pygame.Rect(player_rect.x+4, player_rect.y+4, 42*health_ratio, 42)
            if hit_flash > 0:
                pygame.draw.rect(screen, (255,255,255), player_rect,4)
                pygame.draw.rect(screen, (255,255,255), player_hb)
                hit_flash -= 1
            else:
                pygame.draw.rect(screen, po_color, player_rect,4)
                pygame.draw.rect(screen, p_color, player_hb)
            screen.blit(rotated_gun, gun_rect)

        if player_health <= 0:
            if game_over_time is None:
                game_over_time = current_time

            over_text = game_over_font.render("GAME OVER", True, (255,0,0))
            screen.blit(over_text, (screen_width//2 - 300, screen_height//2 - 75))

            if current_time - game_over_time > 5000:
                player_health = 10
                max_health = 10
                player_x = screen_width/2
                player_y = screen_height/2
                score = 0
                fire_bullet = 0
                ricochet = 0
                piercing_bullet = 0
                thorns = 0
                extra_shot = 0
                lifesteal = 0
                knockback = 15
                next_upgrade_score = 3
                next_special_upgrade = 8
                enemies.clear()
                state = "menu"
        score_text = font.render(f"SCORE:{str(score)}", True, (255,255,255))
        screen.blit(score_text, (5, 5))
        score_text = font.render(f"NEXT UPGRADE:{str(next_upgrade_score)}", True, (255,255,255))
        screen.blit(score_text, (5, 28))


    pygame.display.update()
    clock.tick(60) # Limits loop to 60 FPS
pygame.quit()