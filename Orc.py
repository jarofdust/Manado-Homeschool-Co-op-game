import pygame
from orc import Orc 

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

orc = Orc(400, 300)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dx = 0
    dy = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1

    orc.move(dx, dy)
    
    screen.fill((30, 30, 30))
    orc.draw(screen)

    pygame.display.flip()

pygame.quit()

