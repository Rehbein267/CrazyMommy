import pygame
import random
from settings import WIDTH, HEIGHT

class Explosion(pygame.sprite.Group):
    """Animação de explosão com partículas, flash e som."""

    def __init__(self, center, screen, sfx_expl=None):
        super().__init__()
        self.center = center
        self.screen = screen
        self.sfx_expl = sfx_expl

        if self.sfx_expl:
            self.sfx_expl.set_volume(0.8)
            self.sfx_expl.play()

        for _ in range(30):
            self.add(Particle(center))

        self.flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.flash_surface.fill((255, 255, 255, 200))
        self.flash_timer = pygame.time.get_ticks()

    def update(self):
        super().update()
        for p in list(self):
            if not p.alive:
                self.remove(p)

    def draw(self, surface):
        for p in self:
            surface.blit(p.image, p.rect)

    def draw_flash(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.flash_timer
        if elapsed < 180:
            alpha = max(0, 200 - (elapsed * 2))
            self.flash_surface.set_alpha(alpha)
            self.screen.blit(self.flash_surface, (0, 0))


class Particle(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        size = random.randint(6, 12)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = random.choice([
            (255, 255, 80),
            (255, 140, 0),
            (255, 60, 60),
            (255, 255, 255),
        ])
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=center)

        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-6, 2)
        self.gravity = 0.25
        self.life = random.randint(500, 1000)
        self.spawn_time = pygame.time.get_ticks()
        self.alive = True

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.spawn_time
        if elapsed > self.life:
            self.alive = False
            return

        self.vy += self.gravity
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        fade_ratio = 1 - (elapsed / self.life)
        alpha = int(255 * fade_ratio)
        self.image.set_alpha(alpha)
