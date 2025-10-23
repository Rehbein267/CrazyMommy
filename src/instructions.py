import pygame
from utils import resource_path
from settings import WIDTH, HEIGHT

def show_instructions(screen):
    """Mostra instruções de como jogar"""
    try:
        bg = pygame.image.load(resource_path("assets/images/background/battleback1.png")).convert()
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    except Exception as e:
        print(f"Error image not found: {e}")
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((30, 30, 60))

    font_title = pygame.font.SysFont("DejaVu Sans", 50)
    font_text = pygame.font.SysFont("DejaVu Sans", 28)

    seta_esquerda = "\u2190"
    seta_direita = "\u2192"
    seta_cima = "\u2191"

    title = font_title.render("Como Jogar Crazy Mommy", True, (255, 215, 0))

    text_lines = [
        f"Use as {seta_direita} {seta_esquerda} para mover a Mãe.",
        f"Use {seta_cima} para pular",
        "Pressione ESPAÇO para lançar chinelos.",
        "Pressione ESC ou ENTER para voltar ao menu.",
        "",
        "Acerte o alvo (fujão) várias vezes para vencer!",
        "Evite bater nos obstáculos — você perde vida.",
        "Se o tempo acabar, você perde a fase.",
        "Boa sorte, Crazy Mommy!",
    ]

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                    running = False

        screen.blit(bg,(0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        y = 180
        for line in text_lines:
            text = font_text.render(line, True, (255, 255, 255))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 45

        pygame.display.flip()
        clock.tick(60)
