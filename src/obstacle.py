import pygame
import random
from utils import resource_path
from settings import GROUND_Y

class Obstacle(pygame.sprite.Sprite):
    """Obstáculo que aparece no chão e causa dano ao jogador."""

    def __init__(self, x_pos):
        super().__init__()
        self.image = pygame.image.load(resource_path("assets/images/obstacles/plant_enemy_02.png")).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (60, 60))
        self.rect = self.image.get_rect(midbottom=(x_pos, GROUND_Y))
        self.speed = 6

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
