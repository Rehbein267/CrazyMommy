import pygame
import random
from settings import WIDTH, HEIGHT


class Mother(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.frames = [
            pygame.image.load("assets/images/mother_run/mother_run00.png").convert_alpha(),
            pygame.image.load("assets/images/mother_run/mother_run01.png").convert_alpha(),
            pygame.image.load("assets/images/mother_run/mother_run02.png").convert_alpha(),
            pygame.image.load("assets/images/mother_run/mother_run03.png").convert_alpha()
        ]

        self.frames = [pygame.transform.smoothscale(f, (90, 110)) for f in self.frames]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)

        self.direction = 1
        self.speed = 4
        self.animation_speed = 0.55
        self.last_update = pygame.time.get_ticks()

    # --------------------------------------------------------
    def move(self, keys):

        base_speed = 4
        extra_speed = 0

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            extra_speed = 3
        elif keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            extra_speed = -2

        self.speed = base_speed + extra_speed
        self.speed = max(2, min(self.speed, 8))

        moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = -1
            moving = True
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 1
            moving = True

        self.update_animation(moving)

        from settings import WIDTH
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

    # --------------------------------------------------------
    def update_animation(self, moving):
        """Alterna frames de animação automaticamente"""
        now = pygame.time.get_ticks()

        if now - self.last_update > 40:
            self.last_update = now
            self.frame_index += 0.4
            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            frame = self.frames[int(self.frame_index)]
            self.image = pygame.transform.flip(frame, self.direction == -1, False)

# ---------------------------------------------------------------

class Target(pygame.sprite.Sprite):
    """Alvo inimigo com animação (frames individuais), fuga da mãe e pulo automático"""

    def __init__(self, start_pos, x_limits=None, mother=None, move_range=None):
        super().__init__()
        self.mother = mother
        self.alive = True
        self.lives = 20

        try:
            filenames = ["target_00.png", "target_01.png", "target_02.png"]
            self.frames = []
            for name in filenames:
                path = f"assets/images/alvo/{name}"
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (80, 100))
                self.frames.append(img)
            self.image = self.frames[0]
        except Exception as e:
            print(f"Erro ao carregar frames do alvo: {e}")
            img = pygame.Surface((80, 100), pygame.SRCALPHA)
            img.fill((120, 220, 120))
            self.frames = [img]
            self.image = img

        self.rect = self.image.get_rect(midbottom=start_pos)

        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.on_ground = True
        self.ground_y = HEIGHT - 120

        self.current_frame = 0
        self.last_update = 0
        self.anim_interval_ms = 70
        self.direction = 1
        self.blink_until_ms = 0

        if move_range is None:
            if x_limits is not None:
                move_range = x_limits
            else:
                move_range = (200, WIDTH - 50)
        self.min_x, self.max_x = move_range

        self.speed = 3
        self.base_speed = 4
        self.mid_speed  = 6
        self.run_speed  = 9
        self.min_gap = 260
        self.max_gap = 360

        self.obstacles = pygame.sprite.Group()

        print("Target created at:", self.rect.topleft)

    # ------------------------------------------------------
    def jump(self, force=-18):
        """Executa pulo se estiver no chão"""
        if self.on_ground:
            self.vy = force
            self.on_ground = False

    # ------------------------------------------------------
    def take_damage(self):
        """Recebe dano do flip-flop e inicia piscada curta"""
        if not self.alive:
            return
        self.lives -= 1
        print(f"Target hit! Lives remaining: {self.lives}")
        self.blink_until_ms = pygame.time.get_ticks() + 120
        if self.lives <= 0:
            self.alive = False

    # ------------------------------------------------------
    def animate(self):
        """Avança frames da corrida continuamente e espelha pela direção"""
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.anim_interval_ms:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
        frame = self.frames[self.current_frame]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

        if pygame.time.get_ticks() < self.blink_until_ms:
            self.image.set_alpha(150)
        else:
            self.image.set_alpha(255)

    def update(self):
        if not self.alive:
            return
        self.direction = 1
        self.rect.x += self.speed * self.direction
        if self.rect.right > WIDTH - 30:
            self.rect.right = WIDTH - 30
            self.speed = 0

        look_ahead = 90
        if self.on_ground and self.obstacles:
            for ob in self.obstacles:
                dx = ob.rect.left - self.rect.right
                if 0 < dx < look_ahead:
                    self.jump(force=-18 if ob.rect.height < 70 else -20)
                    break

        self.vy += self.gravity
        self.rect.y += self.vy

        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        self.animate()

    # ------------------------------------------------------
    def animate_fall(self):
        """Anima o alvo caindo (usado na fase 1 ao ser derrotado)"""
        self.rect.y += 8
        self.rect.x += random.choice([-1, 0, 1])
        if self.rect.top > HEIGHT:
            self.kill()
            print("Target removed from screen")
            return True
        return False
