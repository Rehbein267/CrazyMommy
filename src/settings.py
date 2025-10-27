import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

GROUND_Y = HEIGHT - 120

HUD_BAR_W = int(WIDTH * 0.33)
HUD_BAR_H = 18

WHITE  = (255, 255, 255)
GRAY   = (60, 60, 60)
GREEN  = (46, 204, 113)
YELLOW = (241, 196, 15)
RED    = (231, 76, 60)
BLUE   = (52, 152, 219)
BLACK  = (0, 0, 0)

pygame.font.init()

try:
    DEFAULT_FONT = "Lucida Sans Typewriter"
    pygame.font.SysFont(DEFAULT_FONT, 24)
except Exception:
    DEFAULT_FONT = pygame.font.get_default_font()

SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.5

DEBUG = False

#  Posso importar assim:
#   from src.settings import WIDTH, HEIGHT, FPS, GREEN, DEFAULT_FONT
# ou importar o módulo inteiro:
#   import src.settings as cfg
#   pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
