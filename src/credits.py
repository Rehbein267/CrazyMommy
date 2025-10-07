import pygame
from settings import WIDTH, HEIGHT

def mostrar_creditos(tela):
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_texto = pygame.font.Font(None, 32)

    tela.fill((10, 10, 30))  # fundo escuro
    titulo = fonte_titulo.render("Créditos", True, (255, 255, 255))
    tela.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 100))

    creditos = [
        "Crazy Mommy © 2025 Jane Rehbein",
        "",
         "🖼️ Arte e Cenários:",
        "Fundos por Nidhoggn (OpenGameArt.org)",
        "Licença: CC0 — Domínio Público",
        "",
        "🎵 Trilha sonora: 'Fuga Eletrônica' por Tecnodono",
        "Licença: CC BY-SA 4.0",
        "Disponível em OpenGameArt.org",
        "",
        "🔊 Efeitos sonoros: Freesound.org (CC0)",
        "",
         "🧠 Tecnologias utilizadas:",
        "Python 3.12 | Pygame | Pymunk",
    ]

    y = 200
    for linha in creditos:
        texto = fonte_texto.render(linha, True, (200, 200, 200))
        tela.blit(texto, (WIDTH // 2 - texto.get_width() // 2, y))
        y += 40

    pygame.display.flip()
    pygame.time.wait(6000)  # mostra por 6 segundos
