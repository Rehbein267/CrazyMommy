import pygame
from src.settings import (
    WIDTH, HEIGHT, FPS, GROUND_Y,
    HUD_BAR_W, HUD_BAR_H, WHITE, GRAY, GREEN, RED, DEFAULT_FONT
)
from src.characters import Mother, Target
from src.flipflop import FlipFlop
from src.explosion import Explosion
from src.utils import resource_path

class GameLevel1:
    """Classe principal da Fase 1."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.explosion_channel = pygame.mixer.Channel(15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Level 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(DEFAULT_FONT, 28)

        try:
            pygame.mixer.music.load(resource_path("assets/sounds/sombatalha.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[Aviso] Erro ao carregar música: {e}")

        self.sfx_throw = self._load_sfx("assets/sounds/FlipFlop_launch.wav")
        self.sfx_hit = self._load_sfx("assets/sounds/target_ouch.wav")
        self.sfx_expl = self._load_sfx("assets/sounds/explosion.flac")

        self.bg_back = pygame.image.load(resource_path("assets/images/background/battleback4.png")).convert()
        self.bg_back = pygame.transform.smoothscale(self.bg_back, (WIDTH, HEIGHT))
        self.bg_back_flip = pygame.transform.flip(self.bg_back, True, False)

        self.bg_front = pygame.image.load(resource_path("assets/images/background/battleback4-1.png")).convert_alpha()
        self.bg_front = pygame.transform.smoothscale(self.bg_front, (WIDTH, HEIGHT))
        self.bg_front_flip = pygame.transform.flip(self.bg_front, True, False)

        self.bg_x = 0
        self.bg_speed = 2

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.mother = Mother((150, GROUND_Y))
        self.target = Target((WIDTH - 280, GROUND_Y), (350, WIDTH - 40), self.mother)
        self.all_sprites.add(self.mother, self.target)

        self.target_lives = 12
        self.max_target_lives = 12
        self.max_time_ms = 15_000
        self.start_ms = pygame.time.get_ticks()

        self.running = True

    def _load_sfx(self, path):
        """Carrega efeito sonoro com tratamento de erro."""
        try:
            return pygame.mixer.Sound(resource_path(path))
        except Exception:
            print(f"[Aviso] Falha ao carregar som: {path}")
            return None

    def _draw_bg(self):
        """Desenha fundo com efeito parallax alternado (flip)."""
        self.bg_x -= self.bg_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(self.bg_back, (self.bg_x, 0))
        self.screen.blit(self.bg_back_flip, (self.bg_x + WIDTH, 0))
        self.screen.blit(self.bg_front, (self.bg_x * 1.5, 0))
        self.screen.blit(self.bg_front_flip, (self.bg_x * 1.5 + WIDTH, 0))

    def _draw_hud(self, remaining_ms):
        """Desenha HUD com barra de vida e tempo."""
        bar_w = HUD_BAR_W
        bar_h = HUD_BAR_H
        x, y = 20, 30

        pygame.draw.rect(self.screen, GRAY, (x, y, bar_w, bar_h), border_radius=6)

        ratio = max(0, min(self.target_lives / self.max_target_lives, 1))
        fill = int(bar_w * ratio)
        color = GREEN if ratio > 0.3 else RED
        pygame.draw.rect(self.screen, color, (x, y, fill, bar_h), border_radius=6)

        text = self.font.render(f"Target: {self.target_lives}/{self.max_target_lives}", True, WHITE)
        self.screen.blit(text, (x + 10, y - 28))

        secs = max(0, remaining_ms // 1000)
        txt_time = self.font.render(f"Time: {secs:02d}s", True, WHITE)
        self.screen.blit(txt_time, (WIDTH - 140, 20))

    def _throw_flipflop(self):
        """Cria e arremessa o chinelo."""
        f = FlipFlop(self.mother.rect.center, +1)
        self.projectiles.add(f)
        self.all_sprites.add(f)
        if self.sfx_throw:
            self.sfx_throw.play()

    def _check_collisions(self):
        """Detecta colisões entre chinelo e alvo."""
        if self.mother.rect.right > self.target.rect.left - 100:
            self.mother.rect.right = self.target.rect.left - 100

        hits = pygame.sprite.spritecollide(self.target, self.projectiles, dokill=True)
        if hits and self.target.alive:
            self.target.take_damage()
            self.target_lives = max(0, self.target_lives - 1)
            if self.sfx_hit:
                self.sfx_hit.play()

            if self.target_lives <= 0:
                self.target.alive = False
                self._explode_target()
                self._end(victory=True)

    def _explode_target(self):
        """Efeito de explosão ao eliminar o alvo."""
        pygame.time.wait(80)
        if self.sfx_expl:
            self.explosion_channel.play(self.sfx_expl)

        boom = Explosion(self.target.rect.center, self.screen, self.sfx_expl)
        start_time = pygame.time.get_ticks()
        duration = 1200

        while pygame.time.get_ticks() - start_time < duration:
            self._draw_bg()
            boom.update()
            boom.draw(self.screen)
            boom.draw_flash()
            self.mother.update_animation(True)
            self.screen.blit(self.mother.image, self.mother.rect)
            pygame.display.flip()
            self.clock.tick(FPS)

    def _end(self, victory: bool):
        """Exibe mensagem final e muda de fase."""
        self.bg_speed = 0
        self._draw_bg()
        self.all_sprites.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        msg = "WINNER! Level 2" if victory else "YOU LOST! TRY AGAIN"
        color = GREEN if victory else RED

        surf = self.font.render(msg, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(surf, rect)
        pygame.display.flip()
        pygame.time.wait(1500)
        pygame.mixer.music.stop()

        if victory:
            from src.level2 import GameLevel2
            GameLevel2().run()
        else:
            from src.menu import Menu
            Menu().run()

        self.running = False

    def run(self):
        """Loop principal da fase 1."""
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self._end(victory=False)
                    elif e.key == pygame.K_SPACE:
                        self._throw_flipflop()

            keys = pygame.key.get_pressed()
            self.mother.update(keys)
            self.target.update()
            self.projectiles.update()

            remaining = self.max_time_ms - (pygame.time.get_ticks() - self.start_ms)
            if remaining <= 0:
                self._end(victory=False)

            self._check_collisions()

            self._draw_bg()
            self.all_sprites.draw(self.screen)
            self._draw_hud(remaining)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
