import pygame
from settings import WIDTH, HEIGHT

def show_credits(screen):
    """Exibe os créditos finais rolando na tela sem sobrepor o título"""

    font_title = pygame.font.SysFont("Lucida Sans Typewriter", 48)
    font_text = pygame.font.SysFont("Lucida Sans Typewriter", 28)

    title = font_title.render("Créditos — Crazy Mommy", True, (255, 215, 0))
    title_y = 80
    title_rect = title.get_rect(center=(WIDTH // 2, title_y + title.get_height() // 2))

    credits = [
        "Crazy Mommy © 2025 — Jane Rehbein",
        "",
        "Arte e Cenários:",
        "Backgrounds — Nidhoggn (OpenGameArt.org)",
        "Licença: CC0 — Domínio Público",
        "tiny_cat_sprite — Segel (CC0, OpenGameArt.org)",
        "plantenemies_battlers_charset — NettySvit (CC0, OpenGameArt.org)",
        "DG2D_FREE_v1 — LarryIRL (CC0, OpenGameArt.org)",
        "Girl1.png — jcrown41 (CC0, OpenGameArt.org)",
        "Char001.png — Hyptosis (CC0, OpenGameArt.org)",
        "footgear-flare_20201217 — AntumDeluge (CC0, OpenGameArt.org)",
        "",
        "Trilha Sonora:",
        "'Shaded Woods' — rebrie18 (Freesound.org)",
        "Licença: CC BY 3.0",
        "Boss Battle #1 V1.wav — nene (CC0, OpenGameArt.org)",
        "",
        "Efeitos Sonoros:",
        "Huge Explosion — SamsterBirdies (CC0, Freesound.org)",
        "Laughing (male) — dastudiospr (CC0, Freesound.org)",
        "Hit / Ouch — zeteny_zpx (CC0, Freesound.org)",
        "Oh No — reison55 (CC0, Freesound.org)",
        "BaDoink — BaDoink (CC0, Freesound.org)",
        "Lasso Rope Spin — zapsplat.com (CC0, Freesound.org)",
        "Female Laugh (short) — thedialogueproject (CC0, Freesound.org)",
        "Uh Oh — Ant103010 (CC0, Freesound.org)",
        "awesomeness — mrpoly (CC0, OpenGameArt.org)",
        "winneris.ogg — congusbongus (CC0, OpenGameArt.org)",
        "",
        "Tecnologias:",
        "Python 3.12 | Pygame | Pymunk",
        "",
        "Obrigada por jogar Crazy Mommy!",
    ]

    scroll_y = HEIGHT
    scroll_speed = 1
    safe_top = title_rect.bottom + 28

    running = True
    clock = pygame.time.Clock()

    try:
        pygame.mixer.music.load("assets/sounds/menutheme.wav")
        pygame.mixer.music.play(-1)
    except:
        print("Música de créditos não encontrada.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                running = False

        screen.fill((10, 10, 30))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, title_y))

        y = scroll_y
        for line in credits:
            text = font_text.render(line, True, (200, 200, 200))
            text_rect = text.get_rect(center=(WIDTH // 2, y))
            if text_rect.bottom > safe_top:  # não desenha sobre o título
                screen.blit(text, text_rect)
            y += 40

        scroll_y -= scroll_speed

        if y < safe_top:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()

    from menu import Menu
    Menu().run()
