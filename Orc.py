import pygame
from orc import Orc   #Import the Orc class

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#Create the Orc (outside the loop)
orc = Orc(400, 300)

running = True
while running:
    clock.tick(60)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- MOVEMENT --------
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

    #Move the Orc
    orc.move(dx, dy)

    # -------- DRAW --------
    screen.fill((30, 30, 30))
    orc.draw(screen)

    pygame.display.flip()

pygame.quit()
