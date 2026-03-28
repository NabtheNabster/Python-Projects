import pygame
pygame.init()
cube = pygame.image.load("geodashicon.png")
spike_image = pygame.image.load("spike.png")
screen = pygame.display.set_mode((1300,700))
screen_width = screen.get_width()
screen_height = screen.get_height()
alive = True
ground_rect = pygame.Rect(0, screen_height/2 + 50, screen_width, screen_height/2 - 50)
font = pygame.font.Font(None, 100)
death_time = 0
respawn_delay = 1500
attempts = 1
text_x = 300


class Player:
    def __init__(self, x, y, vely, velx):
        self.x = x
        self.y = y
        self.vely = vely
        self.velx = velx
        self.size = 50  # collision size
        self.display_size = 100  # display size for larger image
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

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.base_image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
        screen.blit(rotated_image, rotated_rect.topleft)
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
        global alive, attempts , death_time, scroll_speed
        spike_rect = pygame.Rect(self.x, self.y, self.display_size-30, self.display_size-10)
        if spike_rect.colliderect(player_rect) and alive:
            alive = False
            death_time = current_time
            scroll_speed = 0

    def draw(self, screen):
        screen.blit(self.base_image, (self.x, self.y))

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
            if event.key == pygame.K_SPACE:
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
        player_rect = player.draw(screen)
    else:
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)

    for s in spikes[:]:
        s[0] -= scroll_speed
        spike = Spike(s[0], s[1])
        spike.collision(player_rect)
        spike.draw(screen)
        if s[0] < -100:
            spikes.remove(s)
    for s in spikes[:]:
        spike = Spike(s[0] + 50, s[1])
        spike.collision(player_rect)
        spike.draw(screen)
        if s[0] < -100:
            spikes.remove(s)
    for s in spikes[:]:
        spike = Spike(s[0] + 100, s[1])
        spike.collision(player_rect)
        spike.draw(screen)
        if s[0] < -100:
            spikes.remove(s)

    if len(spikes) == 0 or spikes[-1][0] < screen_width - 300:
        spikes.append([screen_width + 100, screen_height/2])
    text_x -= scroll_speed

    screen.blit(
        font.render("Attempt: {}".format(attempts), True, (255, 255, 255)),
        (text_x, 50)
    )
    pygame.draw.rect(screen, (0,0,255), ground_rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()