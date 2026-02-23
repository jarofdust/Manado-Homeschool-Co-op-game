import pygame
import os

class Orc:
    def __init__(self, x, y):
        self.health = 100
        self.attack_damage = 20
        self.speed = 4

        base_dir = os.path.dirname(__file__)

        self.images = {
            "left": pygame.image.load(os.path.join(base_dir, "LeftwalkingOrc.png")).convert_alpha(),
            "right": pygame.image.load(os.path.join(base_dir, "RightwalkingOrc.png")).convert_alpha(),
            "down": pygame.image.load(os.path.join(base_dir, "FrontFacingOrc.png")).convert_alpha(),
            "up": pygame.image.load(os.path.join(base_dir, "BackFacingOrc.png")).convert_alpha(),
        }

        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, dx, dy):
        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"

        self.image = self.images[self.direction]

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def attack(self, target):
        if self.rect.colliderect(target.rect):
            target.take_damage(self.attack_damage)
            running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))   # background color

    # draw things here
    # example:
    # orc.draw(screen)

    pygame.display.flip()  # 🔥 THIS shows everything on screen

pygame.quit()