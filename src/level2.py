import pygame
import random
from settings import WIDTH, HEIGHT, FPS
from characters import Mother, Target
from flipflop import FlipFlop
from credits import show_credits

# ============================================================
class Obstacle(pygame.sprite.Sprite):
    """Cria obstáculos aleatórios alinhados ao chão"""
    def __init__(self, x):
        super().__init__()
        obstacle_images = [
            ("assets/images/obstacles/plant_enemy_01.png", (70, 50)),
            ("assets/images/obstacles/plant_enemy_02.png", (70, 50)),
            ("assets/images/obstacles/plant_enemy_07.png", (70, 50)),
            ("assets/images/obstacles/goat.png", (80, 60)),
            ("assets/images/obstacles/plant_enemy_08.png", (80, 60)),
        ]
        path, size = random.choice(obstacle_images)
        try:
            img = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.smoothscale(img, size)
        except Exception:
            self.image = pygame.Surface(size)
            self.image.fill((200, 60, 60))
        ground_y = HEIGHT - 120
        self.rect = self.image.get_rect(midbottom=(x, ground_y))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

# ============================================================
class GameLevel2:
    """Fase 2 — obstáculos, barra de vida, cronômetro e créditos"""
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Level 2")
        self.clock = pygame.time.Clock()

        try:
            pygame.mixer.music.load("assets/sounds/sombatalha.wav")
            pygame.mixer.music.play(-1)
        except:
            print("Música de fundo não carregada.")

        try:
            self.sound_hit = pygame.mixer.Sound("assets/sounds/target_ouch.wav")
            self.sound_hit.set_volume(0.6)
        except:
            self.sound_hit = None

        raw_frames = [
            "assets/images/background/battleback2.png",
            "assets/images/background/battleback2-1.png",
            "assets/images/background/battleback2-2.png",
            "assets/images/background/battleback2-3.png"
        ]

        self.bg_frames = [pygame.transform.smoothscale(pygame.image.load(p).convert(), (WIDTH, HEIGHT)) for p in raw_frames]
        self.bg_frames_flipped = [pygame.transform.flip(img, True, False) for img in self.bg_frames]

        self.bg_index = 0
        self.bg_next_index = 1
        self.bg_alpha = 0
        self.bg_transition_speed = 2
        self.bg_speed = 1.8
        self.bg_x = 0
        self.last_switch = pygame.time.get_ticks()
        self.switch_interval = 6000

        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.flipflops = pygame.sprite.Group()

        self.ground_y = HEIGHT - 120
        self.mother = Mother((180, self.ground_y))
        self.target = Target((WIDTH - 500, self.ground_y), (400, WIDTH - 50), self.mother)
        self.mother.target = self.target
        self.target.obstacles = self.obstacles
        self.all_sprites.add(self.mother, self.target)

        self.running = True
        self.target_health = 50
        self.max_target_health = 50
        self.mother_health = 5
        self.gravity = 0.8
        self.jump_force = -22
        self.mother_velocity_y = 0
        self.mother_can_jump = True

        self.obstacle_timer = 0
        self.last_hit_ms = 0
        self.collision_cooldown_ms = 1000

        self.max_time_ms = 30_000
        self.start_time_ms = pygame.time.get_ticks()

    # -----------------------------------------------------------
    def draw_parallax_background(self):
        """Fundo com transição suave e espelhamento"""
        now = pygame.time.get_ticks()
        if now - self.last_switch > self.switch_interval:
            self.last_switch = now
            self.bg_next_index = (self.bg_index + 1) % len(self.bg_frames)
            self.bg_alpha = 0

        self.bg_x -= self.bg_speed
        if self.bg_x <= -WIDTH:
            self.bg_x = 0

        current_bg = self.bg_frames[self.bg_index]
        next_bg = self.bg_frames[self.bg_next_index]

        self.screen.blit(current_bg, (self.bg_x, 0))
        self.screen.blit(pygame.transform.flip(current_bg, True, False), (self.bg_x + WIDTH, 0))

        if self.bg_alpha < 255:
            blended = next_bg.copy()
            blended.set_alpha(self.bg_alpha)
            self.screen.blit(blended, (self.bg_x, 0))
            self.bg_alpha += self.bg_transition_speed
        else:
            self.bg_index = self.bg_next_index

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((160, 200, 255, 45))
        self.screen.blit(overlay, (0, 0))

    # -----------------------------------------------------------
    def run(self):
        """Loop principal da fase"""
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.running = False
                        pygame.display.quit()
                        from menu import Menu
                        Menu().run()
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
            self.obstacles.update(self.bg_speed)
            self.flipflops.update()

            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > random.randint(4500, 7000):
                x = WIDTH + random.randint(350, 650)
                obstacle = Obstacle(x)
                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)
                self.obstacle_timer = now

            self.check_collisions()

            remaining_ms = self.max_time_ms - (pygame.time.get_ticks() - self.start_time_ms)
            if remaining_ms <= 0:
                print("Tempo esgotado! A mãe perdeu!")
                self.mother_health = 0
                self.end_level(victory=False)
                break

            if self.target_health <= 0:
                print("Alvo derrotado! Subindo créditos...")
                self.end_level(victory=True)
                break

            self.draw_parallax_background()
            self.all_sprites.draw(self.screen)
            self.draw_hud(remaining_ms)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

    def draw_hud(self, remaining_ms):
        """Desenha as barras de vida e cronômetro"""
        ratio = self.target_health / self.max_target_health
        color = (46, 204, 113) if ratio > 0.6 else (241, 196, 15) if ratio > 0.3 else (231, 76, 60)

        bar_x, bar_y, bar_w, bar_h = WIDTH - 200, 20, 150, 16
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill_w = int(bar_w * ratio)
        pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_w, bar_h), border_radius=6)

        txt_lives = self.font.render(f"Alvo: {self.target_health}/{self.max_target_health}", True, (255, 255, 255))
        self.screen.blit(txt_lives, (bar_x - 95, bar_y - 2))

        mom_ratio = self.mother_health / 5
        mom_color = (52, 152, 219) if mom_ratio > 0.5 else (231, 76, 60)
        pygame.draw.rect(self.screen, (60, 60, 60), (20, 20, 150, 16), border_radius=6)
        fill_mom = int(150 * mom_ratio)
        pygame.draw.rect(self.screen, mom_color, (20, 20, fill_mom, 16), border_radius=6)

        txt_mom = self.font.render(f"Mãe: {self.mother_health}/5", True, (255, 255, 255))
        self.screen.blit(txt_mom, (180, 18))

        seconds = max(0, remaining_ms // 1000)
        txt_time = self.font.render(f"Tempo: {seconds:02d}s", True, (255, 255, 255))
        self.screen.blit(txt_time, (20, 45))
    # -----------------------------------------------------------
    def check_collisions(self):
        """Colisões da mãe e dos chinelos"""
        hits_target = pygame.sprite.spritecollide(self.target, self.flipflops, dokill=True)
        if hits_target:
            self.target_health -= 1
            if self.sound_hit:
                self.sound_hit.play()

        now = pygame.time.get_ticks()
        mother_on_ground = (self.mother.rect.bottom >= self.ground_y - 2)

        if mother_on_ground and (now - self.last_hit_ms) >= self.collision_cooldown_ms:
            for ob in self.obstacles:
                if self.mother.rect.colliderect(ob.rect):
                    self.mother_health -= 1
                    self.last_hit_ms = now
                    if self.sound_hit:
                        self.sound_hit.play()

                    if self.mother_health <= 0:
                        self.game_over()
                    break

    # -----------------------------------------------------------
    def end_level(self, victory=True):
        """Mensagem final + créditos"""
        fonte = pygame.font.Font(None, 72)
        msg = "WINNER!" if victory else "GAME OVER"
        cor = (46, 204, 113) if victory else (231, 76, 60)

        texto = fonte.render(msg, True, cor)
        rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(texto, rect)
        pygame.display.flip()
        pygame.time.wait(2000)

        pygame.mixer.music.stop()
        if victory:
            show_credits(self.screen)
        else:
            from menu import Menu
            Menu().run()

        self.running = False

    def game_over(self):
        """Tela de Game Over"""
        fonte = pygame.font.Font(None, 72)
        texto = fonte.render("GAME OVER!", True, (231, 76, 60))
        rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.fill((0, 0, 0))
        self.screen.blit(texto, rect)
        pygame.display.flip()
        pygame.mixer.music.stop()
        pygame.time.wait(2500)

        from menu import Menu
        Menu().run()

    # -----------------------------------------------------------
    def throw_flipflop(self):
        flip = FlipFlop(self.mother.rect.center, self.mother.direction)
        self.all_sprites.add(flip)
        self.flipflops.add(flip)
