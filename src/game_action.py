import pygame
from settings import WIDTH, HEIGHT, FPS
from characters import Mother, Target
from flipflop import FlipFlop
from explosion import Explosion
from utils import resource_path


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.explosion_channel = pygame.mixer.Channel(15)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Level 1")
        self.clock = pygame.time.Clock()

        pygame.mixer.music.load(resource_path("assets/sounds/sombatalha.wav"))
        pygame.mixer.music.play(-1)

        self.sfx_throw = self._load_sfx(resource_path("assets/sounds/FlipFlop_launch.wav"))
        self.sfx_ouch  = self._load_sfx(resource_path("assets/sounds/target_ouch.wav"))
        self.sfx_expl  = self._load_sfx(resource_path("assets/sounds/explosion.flac"))
        self.snd_expl  = self.sfx_expl

        if self.sfx_expl:
            self.sfx_expl.set_volume(0.8)
            self.explosion_channel.play(self.sfx_expl)
            self.explosion_channel.stop()

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

        ground_y = HEIGHT - 120
        self.mother = Mother((150, ground_y))
        self.target = Target((WIDTH - 280, ground_y), (350, WIDTH - 40), self.mother)
        self.all_sprites.add(self.mother, self.target)

        self.running = True
        self.target.alive = True
        self.target_lives = 12
        self.max_target_lives = 12
        self.time_ms = 15_000
        self.start_ms = pygame.time.get_ticks()

    def _load_sfx(self, path):
        try:
            return pygame.mixer.Sound(path)
        except:
            return None

    def _draw_bg(self):

        self.bg_x -= self.bg_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        self.screen.blit(self.bg_back, (self.bg_x, 0))
        self.screen.blit(self.bg_back_flip, (self.bg_x + WIDTH, 0))

        self.screen.blit(self.bg_front, (self.bg_x * 1.5, 0))
        self.screen.blit(self.bg_front_flip, (self.bg_x * 1.5 + WIDTH, 0))

    def _draw_hud(self, remaining_ms):
        bar_w = WIDTH // 3
        bar_h = 16
        x = 20
        y = 20

        pygame.draw.rect(self.screen, (60, 60, 60), (x, y, bar_w, bar_h), border_radius=6)
        ratio = max(0, min(self.target_lives / self.max_target_lives, 1))
        fill = int(bar_w * ratio)
        pygame.draw.rect(self.screen, (46, 204, 113), (x, y, fill, bar_h), border_radius=6)

        font = pygame.font.Font(None, 28)
        self.screen.blit(font.render(
            f"Lives: {self.target_lives}/{self.max_target_lives}", True, (255, 255, 255)), (x + bar_w + 10, y - 2))

        secs = max(0, remaining_ms // 1000)
        self.screen.blit(font.render(f"Time: {secs:02d}s", True, (255, 255, 255)), (20, 44))

    def _throw_flipflop(self):
        f = FlipFlop(self.mother.rect.center, +1)
        self.projectiles.add(f)
        self.all_sprites.add(f)
        if self.sfx_throw:
            self.sfx_throw.play()

    def _collisions(self):
        if self.mother.rect.right > self.target.rect.left - 100:
            self.mother.rect.right = self.target.rect.left - 100

        hits = pygame.sprite.spritecollide(self.target, self.projectiles, dokill=True)
        if hits and self.target.alive:
            self.target.take_damage()
            self.target_lives = max(0, self.target_lives - 1)
            if self.sfx_ouch:
                self.sfx_ouch.play()

            if self.target_lives <= 0:
                self.target.alive = False
                self._explode_target()
                self._end(victory=True)
                return

    def _explode_target(self):
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
        self.bg_speed = 0
        self._draw_bg()
        self.all_sprites.draw(self.screen)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        msg = "WINNER! LEVEL 2" if victory else "YOU LOST! TRY AGAIN"
        color = (46, 204, 113) if victory else (231, 76, 60)

        font = pygame.font.Font(None, 64)
        surf = font.render(msg, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(surf, rect)
        pygame.display.flip()
        pygame.time.wait(1500)
        pygame.mixer.music.stop()

        if victory:
            import level2
            level2.GameLevel2().run()
        else:
            import menu
            menu.Menu().run()

        self.running = False


    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self._end(victory=False)
                    elif e.key == pygame.K_SPACE:
                        self._throw_flipflop()

            self.mother.update(keys)
            self.target.update()
            self.projectiles.update()

            remaining = self.time_ms - (pygame.time.get_ticks() - self.start_ms)
            if remaining <= 0:
                self._end(victory=False)

            self._collisions()

            self._draw_bg()
            self.all_sprites.draw(self.screen)
            self._draw_hud(remaining)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
