import pygame
import os

class Orc:
    def __init__(self, x, y):
        self.health = 100
        self.attack_damage = 20
        self.speed = 4

        base_dir = os.path.dirname(__file__)

        self.images = {
            "left": pygame.image.load(os.path.join(base_dir, "LeftFacingOrc.png")).convert_alpha(),
            "right": pygame.image.load(os.path.join(base_dir, "RightFacingOrc.png")).convert_alpha(),
            "down": pygame.image.load(os.path.join(base_dir, "FrontFacingOrc.png")).convert_alpha(),
            "up": pygame.image.load(os.path.join(base_dir, "BackFacingOrc.png")).convert_alpha(),
            "damage": pygame.image.load(os.path.join(base_dir, "DamageOrc.png")).convert_alpha(),
        }

        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(x, y))
        self.damaged = False
        self.damage_timer = 0
        self.damage_duration = 10  

    def move(self, dx, dy):
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if dx < 0:
            self.direction = "left"
        elif dx > 0:
            self.direction = "right"
        elif dy < 0:
            self.direction = "up"
        elif dy > 0:
            self.direction = "down"

    def update(self):
        if self.damaged:
            self.image = self.images["damage"]
            self.damage_timer -= 1

            if self.damage_timer <= 0:
                self.damaged = False
        else:
            self.image = self.images[self.direction]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

        self.damaged = True
        self.damage_timer = self.damage_duration

    def attack(self, target):
        if self.rect.colliderect(target.rect):
            target.take_damage(self.attack_damage)
