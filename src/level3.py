import pygame
import random
from src.settings import (
    WIDTH, HEIGHT, FPS, GROUND_Y, DEFAULT_FONT,
    HUD_BAR_W, HUD_BAR_H, GRAY, GREEN, YELLOW, RED, WHITE
)
from characters import Mother, JumpingTarget
from flipflop import FlipFlop
from explosion import Explosion
from obstacle import Obstacle
from utils import resource_path
from hud import HudDual

class GameLevel3:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.explosion_channel = pygame.mixer.Channel(15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Level 3")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(DEFAULT_FONT, 28)

        try:
            pygame.mixer.music.load(resource_path("assets/sounds/sombatalha.wav"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[ERRO] Falha ao carregar música: {e}")

        def _sfx(path):
            try:
                return pygame.mixer.Sound(resource_path(path))
            except Exception as e:
                print(f"[Aviso] Som ausente: {path} ({e})")
                return None

        self.sfx_throw = _sfx("assets/sounds/FlipFlop_launch.wav")
        self.sfx_hit = _sfx("assets/sounds/target_ouch.wav")
        self.sfx_expl = _sfx("assets/sounds/explosion.flac")

        self.bg_back = pygame.image.load(resource_path("assets/images/background/battleback3-1.png")).convert()
        self.bg_back = pygame.transform.smoothscale(self.bg_back, (WIDTH, HEIGHT))
        self.bg_back_flip = pygame.transform.flip(self.bg_back, True, False)

        self.bg_front = pygame.image.load(resource_path("assets/images/background/battleback3-2.png")).convert_alpha()
        self.bg_front = pygame.transform.smoothscale(self.bg_front, (WIDTH, HEIGHT))
        self.bg_front_flip = pygame.transform.flip(self.bg_front, True, False)

        self.bg_x = 0
        self.bg_front_x = 0
        self.bg_speed = 2

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.hud = HudDual()

        self.mother = Mother((180, GROUND_Y))
        self.target = JumpingTarget((WIDTH - 200, GROUND_Y), max_lives=20)
        self.all_sprites.add(self.mother, self.target)

        self.mother_lives = getattr(self.mother, "lives", 5)
        self.max_target_lives = 20
        self.max_time_ms = 15_000
        self.start_ms = pygame.time.get_ticks()

        self.obstacle_timer = pygame.time.get_ticks() + 2000
        self.running = True
        self.ended = False

    def _draw_bg(self):
        """Desenha o fundo com flip alternado (sem emendas) e o capim frontal."""
        self.bg_x -= self.bg_speed
        self.bg_front_x -= self.bg_speed * 1.5

        if self.bg_x <= -WIDTH:
            self.bg_x = 0
        if self.bg_front_x <= -WIDTH:
            self.bg_front_x = 0

        self.screen.blit(self.bg_back, (self.bg_x, 0))
        self.screen.blit(self.bg_back_flip, (self.bg_x + WIDTH, 0))

        self.screen.blit(self.bg_front, (self.bg_front_x, 0))
        self.screen.blit(self.bg_front_flip, (self.bg_front_x + WIDTH, 0))

    def _spawn_obstacles(self):
        """Gera obstáculos periodicamente."""
        now = pygame.time.get_ticks()
        if now > self.obstacle_timer:
            x_pos = random.randint(WIDTH + 100, WIDTH + 400)
            obs = Obstacle(x_pos)
            self.obstacles.add(obs)
            self.all_sprites.add(obs)
            self.obstacle_timer = now + random.randint(2500, 4000)

    def _check_collisions(self):
        """Detecta colisão da mãe com obstáculos e reduz vida."""
        hits = pygame.sprite.spritecollide(self.mother, self.obstacles, False)
        if hits:
            self.mother_lives = max(0, self.mother_lives - 1)
            for h in hits:
                h.kill()
            if self.mother_lives == 0:
                self._lose()

    def _throw_flipflop(self):
        """Cria e arremessa o chinelo."""
        f = FlipFlop(self.mother.rect.center)
        self.projectiles.add(f)
        self.all_sprites.add(f)
        if self.sfx_throw:
            self.sfx_throw.play()

    def _check_hits(self):
        """Verifica se o chinelo atingiu o alvo."""
        hits = pygame.sprite.spritecollide(
            self.target, self.projectiles, dokill=True, collided=pygame.sprite.collide_mask
        )
        if hits and self.target.alive:
            self.target.take_damage()
            if self.sfx_hit:
                self.sfx_hit.play()
            if self.target.lives <= 0:
                self._win()

        if self.mother.rect.right > self.target.rect.left - 12:
            self.mother.rect.right = self.target.rect.left - 12

    def _freeze_overlay_msg(self, text, color):
        self.bg_speed = 0
        self._draw_bg()
        self.all_sprites.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        surf = pygame.font.SysFont(DEFAULT_FONT, 52).render(text, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(surf, rect)
        pygame.display.flip()
        pygame.time.wait(1500)

    def _win(self):
        if self.ended:
            return
        self.ended = True

        pygame.time.wait(200)
        if self.sfx_expl:
            self.explosion_channel.play(self.sfx_expl)

        boom = Explosion(self.target.rect.center, self.screen, self.sfx_expl)
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 1500:
            self._draw_bg()
            self.mother.update_animation(True)
            self.screen.blit(self.mother.image, self.mother.rect)
            boom.update()
            boom.draw(self.screen)
            boom.draw_flash()
            pygame.display.flip()
            self.clock.tick(FPS)

        self._freeze_overlay_msg("WINNER!", GREEN)

        pygame.mixer.music.stop()
        try:
            from credits import show_credits
            show_credits(self.screen)
        except Exception as e:
            print(f"Erro ao mostrar créditos: {e}")

        try:
            from menu import Menu
            Menu().run()
        except Exception as e:
            print(f"Erro ao retornar ao menu: {e}")

        self.running = False

    def _lose(self):
        if self.ended:
            return
        self.ended = True
        self._freeze_overlay_msg("YOU LOST! TRY AGAIN", RED)
        pygame.mixer.music.stop()
        from src.menu import Menu
        Menu().run()
        self.running = False

    def run(self):
        """Loop principal da fase."""
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        from src.menu import Menu
                        Menu().run()
                        self.running = False
                    elif e.key == pygame.K_SPACE:
                        self._throw_flipflop()
                    elif e.key == pygame.K_UP and getattr(self.mother, "on_ground", True):
                        self.mother.vy = getattr(self.mother, "jump_force", -25)
                        self.mother.on_ground = False

            keys = pygame.key.get_pressed()
            self.mother.update(keys)
            self.target.update()
            self.projectiles.update()
            self._spawn_obstacles()
            self._check_collisions()
            self._check_hits()
            self.obstacles.update()

            for obs in self.obstacles:
                if self.target.rect.left - obs.rect.right < 120 and self.target.on_ground:
                    self.target.vy = -20
                    self.target.on_ground = False

            elapsed = pygame.time.get_ticks() - self.start_ms
            remaining = max(0, self.max_time_ms - elapsed)
            if remaining == 0:
                self._lose()
                break

            self._draw_bg()
            self.all_sprites.draw(self.screen)
            self.hud.draw(self, remaining)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
