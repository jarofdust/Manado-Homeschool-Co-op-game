import pygame
import os
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True


class Player:
    def __init__(self, x, y):
        self.health = 100
        self.speed = 4
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Orc:
    def __init__(self, x, y, player):
        self.player = player
        self.health = 100
        self.attack_damage = 10
        self.speed = 2

        base_dir = os.getcwd()

        def load_orc_image(name, color):
            path = os.path.join(base_dir, name)
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            s = pygame.Surface((60, 60))
            s.fill(color)
            return s

        self.images = {
            "left": load_orc_image("LeftFacingOrc.png", (255, 0, 0)),
            "right": load_orc_image("RightFacingOrc.png", (0, 255, 0)),
            "down": load_orc_image("FrontFacingOrc.png", (0, 0, 255)),
            "up": load_orc_image("BackFacingOrc.png", (255, 255, 0)),
            "damage": load_orc_image("DamageOrc.png", (255, 0, 255)),
        }

        self.direction = "down"
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(center=(x, y))

        self.damaged = False
        self.damage_timer = 0
        self.damage_duration = 15
        self.attack_cooldown = 60
        self.attack_timer = 0

    def chase(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"

    def attack(self):
        if self.rect.colliderect(self.player.rect) and self.attack_timer <= 0:
            self.player.take_damage(self.attack_damage)
            self.attack_timer = self.attack_cooldown

    def take_damage(self, amount):
        self.health -= amount
        self.damaged = True
        self.damage_timer = self.damage_duration

        dx = self.rect.centerx - self.player.rect.centerx
        dy = self.rect.centery - self.player.rect.centery
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance
            self.rect.x += dx * 5
            self.rect.y += dy * 5

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        self.chase()
        self.attack()

        if self.damaged:
            self.image = self.images["damage"]
            self.damage_timer -= 1
            if self.damage_timer <= 0:
                self.damaged = False
        else:
            self.image = self.images[self.direction]

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player(200, 300)
orc = Orc(500, 300, player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                orc.take_damage(20)

    player.move()
    orc.update()

    screen.fill((0, 0, 0))
    player.draw(screen)
    orc.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
