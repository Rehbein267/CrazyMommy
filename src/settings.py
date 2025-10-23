import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

GROUND_Y = HEIGHT - 120

HUD_BAR_W = int(WIDTH * 0.33)
HUD_BAR_H = 18

WHITE = (255, 255, 255)
GRAY  = (60, 60, 60)
GREEN = (46, 204, 113)
YELLOW= (241, 196, 15)
RED   = (231, 76, 60)

pygame.font.init()
try:
    DEFAULT_FONT = "Lucida Sans Typewriter"
except:
    DEFAULT_FONT = pygame.font.get_default_font()

