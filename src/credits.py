import pygame
from utils import resource_path
from settings import WIDTH, HEIGHT, FPS

def show_credits(screen):
    """Exibe os créditos finais rolando na tela sem sobrepor o título"""
    clock = pygame.time.Clock()
    font_text = pygame.font.SysFont("Lucida Sans Typewriter", 30)

    try:
        bg = pygame.image.load(resource_path("assets/images/background/MenuBg.png")).convert()
        bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
    except:
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill((10, 10, 30))

    title_font = pygame.font.SysFont("Lucida Sans Typewriter", 48, bold=True)
    title_text = title_font.render("Créditos — Crazy Mommy", True, (255, 255, 120))
    title_shadow = title_font.render("Créditos — Crazy Mommy", True, (60, 60, 20))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
    screen.blit(title_text, title_rect)

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
        "oh yes!.wav —Reitanna(CC0, Freesound.org)",
        "oh.wav — Reitanna (CC0, Freesound.org)",
        "awesomeness — mrpoly (CC0, OpenGameArt.org)",
        "winneris.ogg — congusbongus (CC0, OpenGameArt.org)",
        "",
        "Tecnologias:",
        "Python 3.12 | Pygame | Pymunk",
        "",
        "Obrigada por jogar Crazy Mommy!",
    ]

    scroll_y = HEIGHT
    scroll_speed = 1.5
    safe_top = title_rect.bottom + 40

    running = True

    try:
        pygame.mixer.music.load(resource_path("assets/sounds/menutheme.wav"))
        pygame.mixer.music.play(-1)
    except:
        print("Música de créditos não encontrada.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]:
                running = False

        screen.blit(bg,(0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.set_alpha(50)
        overlay.fill((160, 200, 120, 70))
        screen.blit(overlay, (0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))

        y = scroll_y
        for line in credits:
            text = font_text.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y))
            if text_rect.bottom > safe_top:
                screen.blit(text, text_rect)
            y += 40

        scroll_y -= scroll_speed

        if y < safe_top:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()

    return
