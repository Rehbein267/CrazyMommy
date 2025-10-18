import pygame
from settings import WIDTH, HEIGHT


class FlipFlop(pygame.sprite.Sprite):
    """Projétil (flip-flop) lançado pela mãe"""

    def __init__(self, pos, direction):
        super().__init__()

        image = pygame.image.load("assets/images/flipflop1.png").convert_alpha()
        self.image_original = pygame.transform.smoothscale(image, (50, 30))
        self.image = self.image_original
        self.rect = self.image.get_rect(center=pos)

        self.velocity = pygame.Vector2(12 * direction, -10)
        self.gravity = 0.6
        self.angle = 0
        self.direction = direction

    # ----------------------------------------------------------
    def update(self):
        """Movimento de rotação e limpeza quando estiver fora da tela"""

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.velocity.y += self.gravity

        self.angle = (self.angle + 15 * self.direction) % 360
        rotated = pygame.transform.rotate(self.image_original, self.angle)
        self.image = rotated
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
