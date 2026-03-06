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

        base_dir = os.getcwd()

        def load_player_image(name, color):
            path = os.path.join(base_dir, name)
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            s = pygame.Surface((50, 50))
            s.fill(color)
            return s

        self.images = {
            "player": load_player_image("red_knight.png", (0, 255, 255)),
            "player_punching": load_player_image("punching_red_knight.png", (0, 255, 255)),
            "player_jumping": load_player_image("jumping_red_knight.png", (0, 255, 255)),
        }
        self.current_image = self.images["player"]

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
        surface.blit(self.current_image, self.rect)


class Orc:
    def __init__(self, x, y, player):
        self.player = player
        self.health = 50
        self.attack_damage = 10
        self.speed = 2
        self.x = float(x)
        self.y = float(y)

        base_dir = os.getcwd()

        def load_orc_image(name, color):
            path = os.path.join(base_dir, name)
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            s = pygame.Surface((60, 60))
            s.fill(color)
            return s

        self.images = {
            "left": load_orc_image("LeftFacingOrc.png", (0, 255, 0)),
            "right": load_orc_image("RightFacingOrc.png", (0, 255, 0)),
            "down": load_orc_image("FrontFacingOrc.png", (0, 0, 255)),
            "up": load_orc_image("BackFacingOrc.png", (0, 255, 255)),
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

        self.knockback_x = 1
        self.knockback_y = 1

    def chase(self):
        dx = self.player.rect.centerx - self.x
        dy = self.player.rect.centery - self.y
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed

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

        dx = self.x - self.player.rect.centerx
        dy = self.y - self.player.rect.centery
        distance = math.hypot(dx, dy)

        if distance != 0:
            dx /= distance
            dy /= distance
            self.knockback_x = dx * 8
            self.knockback_y = dy * 8

    def update(self):
        if self.attack_timer > 0:
            self.attack_timer -= 1

        if self.knockback_x != 0 or self.knockback_y != 0:
            self.x += self.knockback_x
            self.y += self.knockback_y
            self.knockback_x *= 0.7
            self.knockback_y *= 0.7

            if abs(self.knockback_x) < 0.5:
                self.knockback_x = 0
            if abs(self.knockback_y) < 0.5:
                self.knockback_y = 0

            self.image = self.images["damage"]

        elif self.damaged:
            self.image = self.images["damage"]
            self.damage_timer -= 1
            if self.damage_timer <= 0:
                self.damaged = False

        else:
            self.chase()
            self.attack()
            self.image = self.images[self.direction]

        center = (int(self.x), int(self.y))
        self.rect = self.image.get_rect(center=center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player(200, 300)
orc = Orc(500, 300, player)

attack_range = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dx = player.rect.centerx - orc.rect.centerx
                dy = player.rect.centery - orc.rect.centery
                distance = math.hypot(dx, dy)

                if distance <= attack_range:
                    orc.take_damage(10)

    player.move()
    orc.update()

    screen.fill((0, 0, 0))
    player.draw(screen)
    orc.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
