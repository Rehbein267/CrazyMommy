import pygame, random
from settings import (
    WIDTH, HEIGHT, FPS, GROUND_Y,
    HUD_BAR_W, HUD_BAR_H, WHITE, GRAY, GREEN, YELLOW, RED, DEFAULT_FONT
)
from characters import Mother
from flipflop import FlipFlop
from explosion import Explosion
from utils import resource_path

class JumpingTarget(pygame.sprite.Sprite):
    def __init__(self, start_pos, max_lives=20):
        super().__init__()

        filenames = ["target_00.png", "target_01.png", "target_02.png"]
        self.frames = []
        for name in filenames:
            img = pygame.image.load(resource_path(f"assets/images/alvo/{name}")).convert_alpha()
            img = pygame.transform.smoothscale(img, (80, 100))
            self.frames.append(img)

        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=start_pos)

        self.vy = 0.0
        self.gravity = 1.0
        self.on_ground = True
        self.ground_y = GROUND_Y

        self.lives = max_lives
        self.max_lives = max_lives
        self.alive = True

        self.min_jump = -28
        self.max_jump = -20
        self.jump_cooldown = (600, 1200)
        self.next_jump_at = pygame.time.get_ticks() + random.randint(*self.jump_cooldown)

        self.anim_interval_ms = 60
        self.last_anim = pygame.time.get_ticks()

        self.blink_until = 0
        self.last_hit_time = 0

    def take_damage(self):
        if not self.alive:
            return
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < 150:
            return
        self.last_hit_time = now

        self.lives = max(0, self.lives - 1)
        self.blink_until = now + 150
        if self.lives == 0:
            self.alive = False

    def _maybe_jump(self):
        """Pula em alturas aleatórias, apenas quando está no chão, respeitando cooldown."""
        if not self.on_ground or not self.alive:
            return
        now = pygame.time.get_ticks()
        if now >= self.next_jump_at:
            self.vy = random.uniform(self.min_jump, self.max_jump)
            self.on_ground = False
            self.next_jump_at = now + random.randint(*self.jump_cooldown)

    def _apply_gravity(self):
        self.vy += self.gravity
        self.rect.y += int(self.vy)
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0.0
            self.on_ground = True

    def _animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_anim >= self.anim_interval_ms:
            self.last_anim = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

        if pygame.time.get_ticks() < self.blink_until:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)

    def update(self):
        if not self.alive:
            self.vy = 0.0
        else:
            self._maybe_jump()
            self._apply_gravity()

        self._animate()

class GameLevel2:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.explosion_channel = pygame.mixer.Channel(15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Level 2")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(DEFAULT_FONT, 28)

        try:
            pygame.mixer.music.load(resource_path("assets/sounds/sombatalha.wav"))
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música de fundo: {e}")

        def _sfx(path):
            try:
                return pygame.mixer.Sound(resource_path(path))
            except Exception as e:
                print(f"Erro ao carregar som: {path} ({e})")
                return None

        self.sfx_throw = _sfx("assets/sounds/FlipFlop_launch.wav")
        self.sfx_hit   = _sfx("assets/sounds/target_ouch.wav")
        self.sfx_expl  = _sfx("assets/sounds/explosion.flac")
        self.snd_expl  = self.sfx_expl

        if self.sfx_expl:
            self.sfx_expl.set_volume(0.8)
            self.explosion_channel.play(self.sfx_expl)
            self.explosion_channel.stop()

        self.bg_back = pygame.image.load(resource_path("assets/images/background/battleback2.png")).convert()
        self.bg_back = pygame.transform.smoothscale(self.bg_back, (WIDTH, HEIGHT))
        self.bg_back_flip = pygame.transform.flip(self.bg_back, True, False)

        self.bg_front = pygame.image.load(resource_path("assets/images/background/battleback2-1.png")).convert_alpha()
        self.bg_front = pygame.transform.smoothscale(self.bg_front, (WIDTH, HEIGHT))
        self.bg_front_flip = pygame.transform.flip(self.bg_front, True, False)

        self.bg_x = 0
        self.bg_speed = 2


        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.mother = Mother((180, GROUND_Y))
        self.target = JumpingTarget((WIDTH - 220, GROUND_Y), max_lives=20)

        self.all_sprites.add(self.mother, self.target)

        self.mother_lives = getattr(self.mother, "lives", 5)
        self.max_target_lives = self.target.max_lives
        self.max_time_ms = 15_000
        self.start_ms = pygame.time.get_ticks()

        self.running = True
        self.ended = False

    def _draw_bg(self):
        self.bg_x -= self.bg_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(self.bg_back, (self.bg_x, 0))
        self.screen.blit(self.bg_back_flip, (self.bg_x + WIDTH, 0))

        self.screen.blit(self.bg_front, (self.bg_x * 1.5, 0))
        self.screen.blit(self.bg_front_flip, (self.bg_x * 1.5 + WIDTH, 0))

    def _draw_hud(self, remaining_ms):
        ratio = max(0, min(self.target.lives / self.max_target_lives, 1))
        pygame.draw.rect(self.screen, GRAY,
                         (WIDTH - 20 - HUD_BAR_W, 20, HUD_BAR_W, HUD_BAR_H), border_radius=6)
        fill = int(HUD_BAR_W * ratio)
        color = GREEN if ratio > 0.6 else (YELLOW if ratio > 0.3 else RED)
        pygame.draw.rect(self.screen, color,
                         (WIDTH - 20 - HUD_BAR_W, 20, fill, HUD_BAR_H), border_radius=6)
        self.screen.blit(self.font.render(
            f"Target: {self.target.lives}/{self.max_target_lives}", True, WHITE),
            (WIDTH - 20 - HUD_BAR_W - 180, 18))

        mratio = max(0, min(self.mother_lives / 5, 1))
        pygame.draw.rect(self.screen, GRAY, (20, 20, 150, HUD_BAR_H), border_radius=6)
        pygame.draw.rect(self.screen, (52, 152, 219) if mratio > 0.5 else RED,
                         (20, 20, int(150 * mratio), HUD_BAR_H), border_radius=6)
        self.screen.blit(self.font.render(f"Mom: {self.mother_lives}/5", True, WHITE), (180, 18))

        sec = max(0, remaining_ms // 1000)
        self.screen.blit(self.font.render(f"Time: {sec:02d}s", True, WHITE), (20, 48))

    def _throw_flipflop(self):
        f = FlipFlop(self.mother.rect.center)
        self.projectiles.add(f)
        self.all_sprites.add(f)
        if self.sfx_throw:
            self.sfx_throw.play()

    def _check_hits(self):
        hits = pygame.sprite.spritecollide(self.target, self.projectiles, dokill=True)
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

        pygame.time.wait(80)
        if self.sfx_expl:
            self.explosion_channel.play(self.sfx_expl)

        boom = Explosion(self.target.rect.center, self.screen, self.sfx_expl)
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < 1000:
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
        from credits import show_credits
        show_credits(self.screen)
        import menu
        menu.Menu().run()
        self.running = False

    def _lose(self):
        if self.ended:
            return
        self.ended = True
        self._freeze_overlay_msg("YOU LOST! TRY AGAIN", RED)
        pygame.mixer.music.stop()
        import menu
        menu.Menu().run()
        self.running = False

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.mixer.music.stop()
                        import menu
                        menu.Menu().run()
                    elif e.key == pygame.K_SPACE:
                        self._throw_flipflop()
                    elif e.key == pygame.K_UP and getattr(self.mother, "on_ground", True):
                        self.mother.vy = getattr(self.mother, "jump_force", -25)
                        self.mother.on_ground = False

            keys = pygame.key.get_pressed()
            self.mother.update(keys)
            self.target.update()
            self.projectiles.update()

            elapsed = pygame.time.get_ticks() - self.start_ms
            remaining = max(0, self.max_time_ms - elapsed)
            if remaining == 0:
                self._lose()
                break

            self._check_hits()
            self._draw_bg()
            self.all_sprites.draw(self.screen)
            self._draw_hud(remaining)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
