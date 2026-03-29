import pygame
import random
import math
pygame.init()
cube = pygame.image.load("geodashicon.png")
spike_image = pygame.image.load("spike.png")
screen = pygame.display.set_mode((1300,700))
screen_width = screen.get_width()
screen_height = screen.get_height()
alive = True
ground_rect = pygame.Rect(0, screen_height/2 + 50, screen_width+16, screen_height/2 - 34)
font = pygame.font.Font(None, 100)
death_time = 0
respawn_delay = 1500
attempts = 1
text_x = 300
particles = []
shake_duration = 0   # how many frames left to shake
shake_intensity = 0  # how strong the shake is
offset_x = 0
offset_y = 0

class Player:
    def __init__(self, x, y, vely, velx):
        self.x = x
        self.y = y
        self.vely = vely
        self.velx = velx
        self.size = 50  # collision size
        self.display_size = 50  # display size for larger image
        self.angle = 0
        self.on_ground = False
        # surface for player that can be transformed
        self.base_image = pygame.transform.scale(cube, (self.display_size, self.display_size))

    def movement(self):
        if alive:
            # Apply vertical motion
            self.y += self.vely

            # Ground collision handling
            if self.y + self.size >= ground_rect.top:
                self.y = ground_rect.top - self.size
                self.vely = 0
                self.on_ground = True
                self.angle = round(self.angle / 90) * 90
            else:
                self.on_ground = False
                self.angle = (self.angle - 6) % 360

    def gravity(self):
        if alive and not self.on_ground:
            self.vely += 1

    def jump(self, jump_height):
        if alive and self.on_ground:
            self.vely = -jump_height
            self.on_ground = False

    def draw(self, screen, offset_x, offset_y):
        rotated_image = pygame.transform.rotate(self.base_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
        screen.blit(rotated_image, (rotated_rect.topleft[0] + offset_x, rotated_rect.topleft[1] + offset_y))
        # Return collision rect (display size, centered on player position)
        collision_rect = pygame.Rect(self.x + self.size / 2 - self.display_size / 2, 
                                      self.y + self.size / 2 - self.display_size / 2, 
                                      self.display_size, self.display_size)
        return pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20)

class Spike:
    def __init__(self, x , y):        
        self.x = x
        self.y = y
        self.display_size = 50
        self.base_image = pygame.transform.scale(spike_image, (self.display_size, self.display_size))

    def collision(self, player_rect):
        global alive, attempts , death_time, scroll_speed, shake_duration, shake_intensity
        spike_rect = pygame.Rect(self.x, self.y, self.display_size-30, self.display_size-10)
        if spike_rect.colliderect(player_rect) and alive:
            alive = False
            death_time = current_time
            scroll_speed = 0
            shake_duration = 15     
            shake_intensity = 8  
            for i in range(25):
                angle = random.uniform(0, 2 * math.pi)  # random direction
                speed = random.uniform(4, 12)            # how fast it explodes
                center_x = player.x + player.size / 2
                center_y = player.y + player.size / 2
                vel_x = math.cos(angle) * speed
                vel_y = math.sin(angle) * speed
                particles.append([center_x + random.randint(-25, 25), center_y + random.randint(-25, 25), vel_x, vel_y, random.randint(3, 8)])

    def draw(self, screen, offset_x, offset_y):
        screen.blit(self.base_image, (self.x + offset_x, self.y + offset_y))

scroll_speed = 8.3
player = Player(100, screen_height/2, 0, 0)
spikes = [[screen_width + 200, screen_height/2]]

pygame.display.set_caption("Geometry Dash")
clock = pygame.time.Clock() 
running = True

while running:
    current_time = pygame.time.get_ticks()
    if not alive and current_time - death_time >= respawn_delay:
        attempts += 1
        alive = True
        scroll_speed = 8.3
        player.x = 100
        player.y = screen_height/2
        player.vely = 0
        player.angle = 0
        text_x = 300
        spikes.clear()
        spikes.append([screen_width + 200, screen_height/2])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            player.jump(15)
        if event.type == pygame.MOUSEBUTTONDOWN :
            player.jump(15)
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
        player.jump(15)

    screen.fill((0,0,0))
    if alive == True:
        player.gravity()
        player.movement()
        player_rect = player.draw(screen, offset_x, offset_y)
    else:
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)

    offsets = [0, 50, 100]

    for s in spikes[:]:
        s[0] -= scroll_speed

        for spike_offset in offsets:
            spike = Spike(s[0] + spike_offset, s[1])
            spike.collision(player_rect)
            spike.draw(screen, offset_x, offset_y)

        if s[0] < -100:
            spikes.remove(s)
    for p in particles[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[3] += 0.3  # gravity
        p[4] -= 0.2  # shrink
        p[2] *= 0.98

        if p[4] <= 0:
            particles.remove(p)
        pygame.draw.rect(screen, (255,255,0), (p[0], p[1], p[4], p[4]))
    if alive and player.on_ground:
        particles.append([
            (player.x + player.size / 2) - 25,   # center x
            player.y + player.size,       # bottom of cube
            random.uniform(-3, 0),        # slight sideways drift
            random.uniform(-2, -1),       # upward motion
            random.randint(2, 4),         # small size
            (0, 0, 255)               # color
        ])
        for p in particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.15   # softer gravity
            p[2] *= 0.95   # horizontal slowdown
            p[4] -= 0.1    # slower shrink
            if p[4] <= 0:
                particles.remove(p)
            pygame.draw.rect(screen, (0,255,255), (p[0], p[1], p[4], p[4]))
    if len(spikes) == 0 or spikes[-1][0] < screen_width - 300:
        spikes.append([screen_width + 100, screen_height/2])
    text_x -= scroll_speed

    screen.blit(
        font.render("Attempt: {}".format(attempts), True, (255, 255, 255)),
        (text_x, 50)
    )
    if shake_duration > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_duration -= 1
    else:
        offset_x = 0
        offset_y = 0
    ground_rect = pygame.Rect(0+offset_x, screen_height/2 + 50 + offset_y, screen_width+16, screen_height/2 - 34)
    pygame.draw.rect(screen, (0,0,255), ground_rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()