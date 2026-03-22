import pygame
import json
pygame.init()
running = True
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("todolist")
try:
    with open("tasks.txt", "r") as f:
        tasks = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    tasks = []
    while running:
        pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()
with open("tasks.txt", "w") as f:
    json.dump(tasks, f)