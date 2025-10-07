import pygame
from settings import WIDTH, HEIGHT

def carregar_fundo(background):
    """Carrega e ajusta o fundo do jogo"""
    caminho = f"assets/images/backgrounds/{background}"
    fundo = pygame.image.load(caminho).convert()
    fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))
    return fundo
