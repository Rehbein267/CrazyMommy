import pygame
import random


class Particle(pygame.sprite.Sprite):
    """Pequena partícula colorida"""

    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((4, 4), pygame.SRCALPHA)
        color = random.choice([
            (255, 255, 255),   # branco
            (255, 255, 120),   # amrelo
            (255, 200, 50),    # ouro
            (255, 100, 150),   # rosa
            (150, 200, 255)    # azul fraco
        ])
        pygame.draw.circle(self.image, color, (2, 2), 2)
        self.rect = self.image.get_rect(center=pos)

        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-6, -2)
        self.life = random.randint(20, 40)
        self.gravity = 0.3

    # ----------------------------------------------------------
    def update(self):
        """Gravidade e movimento da particula"""
        self.vel_y += self.gravity
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.life -= 1
        if self.life <= 0:
            self.kill()


# =========================================================
class Explosion(pygame.sprite.Group):
    """Explosão de partículas e efeito de flash brilhante"""

    def __init__(self, pos, screen, explosion_sound=("assets/sounds/explosion.flac")):
        super().__init__()
        self.screen = screen

        for _ in range(30):
            self.add(Particle(pos))

        self.flash_timer = 8
        self.sound = explosion_sound
        if self.sound:
            self.sound.play()
            self.fade_timer = pygame.time.get_ticks() + 200

    # ----------------------------------------------------------
    def draw_flash(self, pos):
        """Desenha um flash rápido e brilhante (efeito de câmera)"""
        if self.flash_timer > 0:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 255, 180, 120), pos, 200)
            self.screen.blit(overlay, (0, 0))
            self.flash_timer -= 1

    # ----------------------------------------------------------
    def update(self):
        """Atualiza partículas e aplica fade-out no som"""
        super().update()

        if hasattr(self, "fade_timer") and self.sound:
            if self.fade_timer is not None and pygame.time.get_ticks() > self.fade_timer:
                self.sound.fadeout(500)
                self.fade_timer = None
