import pygame
import random
import math
pygame.init()

cell_size = 20
cols = 30
rows = 20
apple_pos = [random.randint(0, cols - 1), random.randint(0, rows - 1)]

screen_width = cols * cell_size
screen_height = rows * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake AI Genetic")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
running = True
alive = True
death_time = 0
respawn_delay = 1000
final_apple_per_step = []
final_score = []
testing = True
# Snake
snake_body = [[10, 15]]  # list of [x, y] positions
snake_dir = [1, 0]       # initial direction (dx, dy)
snake_length = 1
steps = 0
# Keep track of how many runs you want
num_runs = 1000
current_run = 0
run = 1
class Brain:
    def __init__(self):
        # weights: 6 inputs → 4 outputs
        self.weights = [[random.uniform(-1,1) for _ in range(6)] for _ in range(4)]

    def activate(self, inputs):
        outputs = []
        for neuron in self.weights:
            total = sum(i*w for i, w in zip(inputs, neuron))
            outputs.append(math.tanh(total))  # activation
        return outputs
outputs = Brain.activate(inputs)
best = outputs.index(max(outputs))

directions = [[0,-1],[0,1],[-1,0],[1,0]]
snake_dir = directions[best]
# --- Main loop ---
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_run < num_runs:
        steps += 1
        head = snake_body[0]
        body = snake_body[1:]

        # --- AI logic ---

        # --- Move snake ---
        new_head = [head[0] + snake_dir[0], head[1] + snake_dir[1]]
        snake_body.insert(0, new_head)
        if len(snake_body) > snake_length:
            snake_body.pop()

        # --- Apple collision ---
        if new_head == apple_pos:
            snake_length += 1
            while apple_pos in snake_body:
                apple_pos = [random.randint(0, cols-1), random.randint(0, rows-1)]

        # --- Death ---
        if new_head in snake_body[1:] or not (0 <= new_head[0] < cols) or not (0 <= new_head[1] < rows):
            final_apple_per_step.append((snake_length-1)/steps if steps>0 else 0)
            final_score.append(snake_length-1)
            current_run += 1
            run += 1
            # respawn
            snake_body = [[10, 15]]
            snake_dir = [1,0]
            snake_length = 1
            steps = 0
            apple_pos = [random.randint(0, cols-1), random.randint(0, rows-1)]

    # --- Draw ---
    screen.fill((0,0,0))
    # draw grid
    for x in range(0, screen_width, cell_size):
        pygame.draw.line(screen, (50,50,50), (x,0), (x,screen_height))
    for y in range(0, screen_height, cell_size):
        pygame.draw.line(screen, (50,50,50), (0,y), (screen_width,y))
    # draw snake
    for seg in snake_body:
        pygame.draw.rect(screen, (0,255,0), (seg[0]*cell_size, seg[1]*cell_size, cell_size, cell_size))
    pygame.draw.rect(screen, (0,200,0), (snake_body[0][0]*cell_size, snake_body[0][1]*cell_size, cell_size, cell_size))
    # draw apple
    pygame.draw.rect(screen, (255,0,0), (apple_pos[0]*cell_size, apple_pos[1]*cell_size, cell_size, cell_size))
    # stats
    screen.blit(font.render(f'Score: {snake_length-1}', True, (255,255,255)), (10,40))
    screen.blit(font.render(f'Apples per step: {((snake_length-1)/steps if steps>0 else 0):.3f}', True, (255,255,255)), (10,10))
    if final_score:
        best_score = max(final_score)
        worst_score = min(final_score)
    else:   
        best_score = 0
        worst_score = 0
    avg_score = sum(final_score)/len(final_score) if final_score else 0
    avg_aps = sum(final_apple_per_step)/len(final_apple_per_step) if final_apple_per_step else 0
    screen.blit(font.render(f'Average Score: {avg_score:.2f}', True, (255,255,255)), (10,70))
    screen.blit(font.render(f'Average Apples per Step: {avg_aps:.3f}', True, (255,255,255)), (10,100))
    screen.blit(font.render(f'Best Score: {best_score}', True, (255,255,255)), (10,130))
    screen.blit(font.render(f'Worst Score: {worst_score}', True, (255,255,255)), (10,160))
    screen.blit(font.render(f'Run: {run}', True, (255,255,255)), (10,190))
    Avg_time_per_run = (current_time/1000)/run if run > 0 else 0
    screen.blit(font.render(f'Average time per run: {Avg_time_per_run:.3f}', True, (255,255,255)), (10,220))
    pygame.display.update()
    clock.tick(100) 