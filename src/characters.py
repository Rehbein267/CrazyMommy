import pygame
import random
from settings import WIDTH, HEIGHT
from utils import resource_path

import pygame


class Mother(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.frames = [
        pygame.image.load(resource_path("assets/images/mother_run/mother_run00.png")).convert_alpha(),
        pygame.image.load(resource_path("assets/images/mother_run/mother_run01.png")).convert_alpha(),
        pygame.image.load(resource_path("assets/images/mother_run/mother_run02.png")).convert_alpha(),
        pygame.image.load(resource_path("assets/images/mother_run/mother_run03.png")).convert_alpha(),
        ]

        self.frames = [pygame.transform.smoothscale(f, (95, 110)) for f in self.frames]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=pos)
        self.frame_index = 0

        self.direction = 1
        self.speed = 4

        self.vy = 0
        self.gravity = 1
        self.jump_force = -25
        self.on_ground = True
        self.ground_y = pos[1]

        self.last_update = pygame.time.get_ticks()

    def move(self, keys):
        moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
            moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1
            moving = True

        if self.on_ground and keys[pygame.K_UP]:
            self.vy = self.jump_force
            self.on_ground = False
        return moving

    def apply_gravity(self):
        self.vy += self.gravity
        self.rect.y += self.vy

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.on_ground = True

    def update_animation(self, moving):
        now = pygame.time.get_ticks()
        if now - self.last_update > 40:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            frame = self.frames[int(self.frame_index)]
            self.image = pygame.transform.flip(frame, self.direction == -1, False)

    def update(self, keys):
        moving = self.move(keys)
        self.apply_gravity()
        self.update_animation(moving)

class Target(pygame.sprite.Sprite):
    """Corre dentro de um intervalo e morre com explosão."""
    def __init__(self, start_pos, move_range, mother=None):
        super().__init__()
        self.mother = mother
        self.alive = True
        self.lives = 20

        filenames = ["target_00.png", "target_01.png", "target_02.png"]
        self.frames = []
        for name in filenames:
            path = f"assets/images/alvo/{name}"
            img = pygame.image.load(resource_path(path)).convert_alpha()
            img = pygame.transform.smoothscale(img, (80, 100))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=start_pos)

        self.min_x, self.max_x = move_range
        self.speed_ground = 3.5
        self.vx_air = 3.5
        self.vy = 0.0
        self.gravity = 0.9
        self.jump_force_base = -26
        self.on_ground = True
        self.ground_y = HEIGHT - 120

        self.anim_interval_ms = 60
        self.last_anim = pygame.time.get_ticks()

        self.blink_until = 0

    def take_damage(self):
        if not self.alive:
            return
        now = pygame.time.get_ticks()
        if hasattr(self, "last_hit_time") and now - self.last_hit_time < 300:
            return
        self.last_hit_time = now

        self.lives -= 1
        self.blink_until = pygame.time.get_ticks() + 150
        if self.lives <= 0:
            self.alive = False

    def update(self):
        if not self.alive:
            self.vx_air = 0
            self.vy = 0
            return

        if self.on_ground:
            self.rect.x += self.speed_ground
        else:
            self.rect.x += self.vx_air * 0.9

        if self.rect.right >= WIDTH - 30:
            self.rect.right = WIDTH - 30
            self.speed_ground = 0

        self.vy += self.gravity
        self.rect.y += int(self.vy)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0.0
            self.on_ground = True

        self._animate()

        if pygame.time.get_ticks() < self.blink_until:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)


    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim >= self.anim_interval_ms:
            self.last_anim = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
