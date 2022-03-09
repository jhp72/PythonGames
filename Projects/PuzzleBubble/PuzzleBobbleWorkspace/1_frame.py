import pygame

pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Bobble")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60) # FPS 60 으로 설정

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()