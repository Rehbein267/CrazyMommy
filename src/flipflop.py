import pygame
import math
from utils import resource_path
from settings import WIDTH, HEIGHT

class FlipFlop(pygame.sprite.Sprite):
    """Chinelo giratório lançado pela mãe."""
    def __init__(self, pos, direction=1):
        super().__init__()

        self.base_image = pygame.image.load(resource_path("assets/images/flipflop1.png")).convert_alpha()
        self.base_image = pygame.transform.smoothscale(self.base_image, (50, 40))
        self.image = self.base_image
        self.rect = self.image.get_rect(center=pos)

        self.direction = direction
        self.angle = 0
        self.spin_speed = 22

        self.vel_x = 14 * direction
        self.vel_y = -12
        self.gravity = 0.7

        try:
            self.throw_sound = pygame.mixer.Sound(resource_path("assets/sounds/flipflop_launch.wav"))
            self.throw_sound.set_volume(0.6)
            self.throw_sound.play()
        except:
            self.throw_sound = None

    def update(self):
        self.rect.x += int(self.vel_x)
        self.rect.y += int(self.vel_y)
        self.vel_y += self.gravity

        self.angle = (self.angle + self.spin_speed) % 360
        rotated = pygame.transform.rotate(self.base_image, self.angle)
        self.image = rotated
        self.rect = self.image.get_rect(center=self.rect.center)

        if (self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT):
            self.kill()
