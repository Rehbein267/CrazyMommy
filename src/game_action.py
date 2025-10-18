import pygame
from settings import WIDTH, HEIGHT, FPS
from characters import Mother, Target
from flipflop import FlipFlop
from explosion import Explosion
import random


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 28)

        pygame.mixer.init()
        self.sound_explosion = self.safe_load_sound("assets/sounds/explosion.flac")
        self.sound_battle = self.safe_load_sound("assets/sounds/sombatalha.wav")
        self.sound_throw = self.safe_load_sound("assets/sounds/FlipFlop_launch.wav")
        self.sound_hit = self.safe_load_sound("assets/sounds/target_ouch.wav")

        try:
            pygame.mixer.music.load("assets/sounds/sombatalha.wav")
            pygame.mixer.music.play(-1)
        except:
            print("Música de fundo não carregada.")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Angry Flip-Flops")
        self.clock = pygame.time.Clock()

        raw_frames = [
            pygame.image.load("assets/images/background/battleback4.png").convert(),
            pygame.image.load("assets/images/background/battleback4-1.png").convert(),
            pygame.image.load("assets/images/background/battleback4-2.png").convert(),
            pygame.image.load("assets/images/background/battleback4-3.png").convert(),
        ]
        self.bg_frames, self.bg_frames_flipped = [], []
        for img in raw_frames:
            scaled = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            self.bg_frames.append(scaled)
            self.bg_frames_flipped.append(pygame.transform.flip(scaled, True, False))

        self.bg_index = 0
        self.bg_last_swap = pygame.time.get_ticks()
        self.bg_anim_ms = 30 * 16
        self.bg_speed = 1.8
        self.bg_x = 0

        self.all_sprites = pygame.sprite.Group()
        self.flipflops = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        ground_y = HEIGHT - 120
        self.mother = Mother((100, ground_y))
        self.target = Target((WIDTH - 150, ground_y), (200, WIDTH - 50), self.mother)
        self.all_sprites.add(self.mother, self.target)

        self.running = True
        self.target_lives = 20
        self.level_completed = False
        self.max_time_ms = 20_000
        self.start_time_ms = pygame.time.get_ticks()
        self.obstacle_timer = 0
        self.target_health = 20
        self.max_target_health = 20
        self.mother_health = 10

        self.gravity = 1
        self.mother_velocity_y = 0
        self.mother_can_jump = True
        self.jump_force = -18

    # -------------------------------------------------------------
    def safe_load_sound(self, path: str):
        """Carrega som sem quebrar o jogo caso falte"""
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Sound not found: {path} — {e}")
            return None

    # -------------------------------------------------------------
    def draw_parallax_background(self):
        """Efeito de parallax com transição e leve"""
        now = pygame.time.get_ticks()
        if now - self.bg_last_swap >= self.bg_anim_ms:
            self.bg_last_swap = now
            self.bg_index = (self.bg_index + 1) % len(self.bg_frames)

        current_bg = self.bg_frames[self.bg_index]
        current_bg_flipped = self.bg_frames_flipped[self.bg_index]

        self.bg_x -= self.bg_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(current_bg, (self.bg_x, 0))
        self.screen.blit(current_bg_flipped, (self.bg_x + WIDTH, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((160, 200, 255, 60))
        self.screen.blit(overlay, (0, 0))

    # -------------------------------------------------------------
    def run(self):
        """Loop principal da fase"""
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    pygame.mixer.music.stop()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        pygame.mixer.music.stop()
                        self.running = False
                        pygame.display.quit()
                        import menu

                        menu.Menu().run()
                    elif e.key == pygame.K_SPACE:
                        self.throw_flipflop()
                    elif e.key == pygame.K_UP and self.mother_can_jump:
                        self.mother_velocity_y = self.jump_force
                        self.mother_can_jump = False

            keys = pygame.key.get_pressed()
            self.mother.move(keys)

            if self.mother.rect.right > self.target.rect.left - 120:
                self.mother.rect.right = self.target.rect.left - 120

            self.mother_velocity_y += self.gravity
            self.mother.rect.y += self.mother_velocity_y
            if self.mother.rect.bottom >= HEIGHT - 120:
                self.mother.rect.bottom = HEIGHT - 120
                self.mother_velocity_y = 0
                self.mother_can_jump = True

            self.target.update()
            self.flipflops.update()

            self.check_collisions()
            if self.level_completed:
                self.end_level(victory=True)

            remaining_ms = self.max_time_ms - (
                pygame.time.get_ticks() - self.start_time_ms
            )
            if remaining_ms <= 0:
                print("Tempo esgotado! A mãe perdeu!")
                self.mother_health = 0
                self.end_level(victory=False)
                break

            self.draw_parallax_background()
            self.all_sprites.draw(self.screen)
            self.draw_hud(remaining_ms)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    # -------------------------------------------------------------
    def throw_flipflop(self):
        """Cria e lança um flip-flop na direção atual da mãe"""
        flip = FlipFlop(self.mother.rect.center, self.mother.direction)
        self.all_sprites.add(flip)
        self.flipflops.add(flip)
        if self.sound_throw:
            self.sound_throw.play()

    # -------------------------------------------------------------
    def check_collisions(self):
        """Detecta acertos e aciona fim da fase quando o alvo morre"""
        if not self.level_completed and self.target_lives > 0:
            hits = pygame.sprite.spritecollide(self.target, self.flipflops, dokill=True)
            if hits:
                self.target.take_damage()
                self.target_lives = max(0, self.target_lives - 1)

                if self.sound_hit:
                    self.sound_hit.play()

                if self.target_lives <= 0 and not self.level_completed:
                    print(" Target defeated!")
                    self.explosion = Explosion(
                        self.target.rect.center, self.screen, self.sound_explosion
                    )
                    for p in self.explosion.sprites():
                        self.all_sprites.add(p)
                    self.level_completed = True

        if hasattr(self, "explosion"):
            self.explosion.update()
            self.explosion.draw(self.screen)
            self.explosion.draw_flash(self.target.rect.center)


    # -------------------------------------------------------------
    def draw_hud(self, remaining_ms: int):
        """Desenha barra de vidas e cronômetro"""
        font = pygame.font.Font(None, 28)
        max_lives = self.max_target_health

        bar_x, bar_y, bar_w, bar_h = 20, 20, 150, 16
        pygame.draw.rect(
            self.screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=6
        )

        ratio = max(0.0, min(self.target_lives / max_lives, 1.0))
        fill_w = int(bar_w * ratio)
        pygame.draw.rect(
            self.screen, (46, 204, 113), (bar_x, bar_y, fill_w, bar_h), border_radius=6
        )

        txt_lives = font.render(
            f"Lives: {self.target_lives}/{max_lives}", True, (255, 255, 255)
        )
        self.screen.blit(txt_lives, (bar_x + bar_w + 10, bar_y - 2))

        seconds = max(0, remaining_ms // 1000)
        txt_time = font.render(f"Time: {seconds:02d}s", True, (255, 255, 255))
        self.screen.blit(txt_time, (20, 44))

    # -------------------------------------------------------------
    def end_level(self, victory=True):
        """Mensagem final + transição segura para a Fase 2 ou Menu"""
        font = pygame.font.Font(None, 64)
        msg = "WINNER! LEVEL 2 LOADING..." if victory else "YOU LOST! TRY AGAIN!"
        color = (46, 204, 113) if victory else (205, 133, 63)

        text = font.render(msg, True, color)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(1600)

        if self.sound_battle:
            self.sound_battle.stop()

        self.running = False
        pygame.display.quit()
        pygame.time.wait(250)
        pygame.display.init()

        if victory:
            print("Loading Level 2...")
            import level2

            level2.GameLevel2().run()
        else:
            print("Returning to main menu...")
            import menu

            menu.Menu().run()
