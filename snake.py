import pygame
import random
pygame.init()

cell_size = 20
cols = 30
rows = 20
apple_pos = [random.randint(0, cols - 1), random.randint(0, rows - 1)]

screen_width = cols * cell_size
screen_height = rows * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake AI")
input_delay = 200  # milliseconds
last_input_time = 0
clock = pygame.time.Clock()
running = True

# Snake
snake_body = [[10, 15]]  # list of [x, y] positions
snake_dir = [1, 0]       # initial direction (dx, dy)
snake_length = 10

while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE,):
                running = False
            if current_time - last_input_time > input_delay:
                if event.key in (pygame.K_UP, pygame.K_w) and snake_dir[1] == 0:
                    snake_dir = [0, -1]
                if event.key in (pygame.K_DOWN, pygame.K_s) and snake_dir[1] == 0:
                    snake_dir = [0, 1]
                if event.key in (pygame.K_LEFT, pygame.K_a) and snake_dir[0] == 0:
                    snake_dir = [-1, 0]
                if event.key in (pygame.K_RIGHT, pygame.K_d) and snake_dir[0] == 0:
                    snake_dir = [1, 0]

    # Move snake
    new_head = [snake_body[0][0] + snake_dir[0], snake_body[0][1] + snake_dir[1]]
    snake_body.insert(0, new_head)  # add new head to front
    if len(snake_body) > snake_length:
        snake_body.pop()  # remove tail if too long
    # Apply simple collision rules (self-collision and wall collision)
    if snake_body[0] in snake_body[1:] or not (0 <= snake_body[0][0] < cols) or not (0 <= snake_body[0][1] < rows):
        running = False
    # Apple
    if apple_pos in snake_body:
        snake_length += 1  # grow snake
        while apple_pos in snake_body:  # ensure new apple doesn't spawn on snake
            apple_pos = [random.randint(0, cols - 1), random.randint(0, rows - 1)]

    # Draw
    screen.fill((0, 0, 0))

    # grid
    for x in range(0, screen_width, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, screen_height))
    for y in range(0, screen_height, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (screen_width, y))

    # draw snake
    for segment in snake_body:
        pygame.draw.rect(screen, (0, 255, 0),
                         (segment[0]*cell_size, segment[1]*cell_size, cell_size, cell_size))
        if segment == snake_body[0]:  
            pygame.draw.rect(screen, (0, 200, 0),
                             (segment[0]*cell_size, segment[1]*cell_size, cell_size, cell_size))
            if snake_body.count(segment) > 1 or not (0 <= segment[0] < cols) or not (0 <= segment[1] < rows):  
                running = False
    # draw apple
    pygame.draw.rect(screen, (255, 0, 0),
                     (apple_pos[0]*cell_size, apple_pos[1]*cell_size, cell_size, cell_size))
            
    pygame.display.update()
    clock.tick(5)