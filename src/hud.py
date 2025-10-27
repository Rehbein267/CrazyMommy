import pygame
from settings import WIDTH, HUD_BAR_W, HUD_BAR_H, GRAY, GREEN, YELLOW, RED, WHITE

class HudStrategy:
    def draw(self, game, remaining_ms):
        raise NotImplementedError

class HudSimple(HudStrategy):
    """
    Level 1 e 2:
    - Tempo centralizado no topo
    - Barra do alvo à direita
    """
    def draw(self, game, remaining_ms):
        bar_w = 180
        bar_h = HUD_BAR_H
        margin_x = 20
        TEXT_Y = 26
        BAR_Y  = 52

        sec = max(0, remaining_ms // 1000)
        time_text = game.font.render(f"Time: {sec:02d}s", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, TEXT_Y))
        game.screen.blit(time_text, time_rect)

        ratio = max(0, min(game.target.lives / game.max_target_lives, 1))
        x_bar = WIDTH - bar_w - margin_x
        pygame.draw.rect(game.screen, GRAY, (x_bar, BAR_Y, bar_w, bar_h), border_radius=6)
        color = GREEN if ratio > 0.6 else (YELLOW if ratio > 0.3 else RED)
        pygame.draw.rect(game.screen, color, (x_bar, BAR_Y, int(bar_w * ratio), bar_h), border_radius=6)

        text = game.font.render(f"Target: {game.target.lives}/{game.max_target_lives}", True, WHITE)
        game.screen.blit(text, (x_bar, BAR_Y - 22))


class HudDual(HudStrategy):
    """
    Level 3:
    - Barra da mãe à esquerda
    - Tempo centralizado no topo
    - Barra do alvo à direita
    """
    def draw(self, game, remaining_ms):
        bar_w = 180
        bar_h = HUD_BAR_H
        margin_x = 20
        TEXT_Y = 26
        BAR_Y  = 52

        mom_ratio = max(0, min(game.mother_lives / 5, 1))
        pygame.draw.rect(game.screen, GRAY, (margin_x, BAR_Y, bar_w, bar_h), border_radius=6)
        mom_color = GREEN if mom_ratio > 0.5 else RED
        pygame.draw.rect(game.screen, mom_color, (margin_x, BAR_Y, int(bar_w * mom_ratio), bar_h), border_radius=6)
        text_mom = game.font.render(f"Mom: {game.mother_lives}/5", True, WHITE)
        game.screen.blit(text_mom, (margin_x, BAR_Y - 22))

        sec = max(0, remaining_ms // 1000)
        time_text = game.font.render(f"Time: {sec:02d}s", True, WHITE)
        time_rect = time_text.get_rect(center=(WIDTH // 2, TEXT_Y))
        game.screen.blit(time_text, time_rect)

        ratio = max(0, min(game.target.lives / game.max_target_lives, 1))
        x_bar = WIDTH - bar_w - margin_x
        pygame.draw.rect(game.screen, GRAY, (x_bar, BAR_Y, bar_w, bar_h), border_radius=6)
        color = GREEN if ratio > 0.6 else (YELLOW if ratio > 0.3 else RED)
        pygame.draw.rect(game.screen, color, (x_bar, BAR_Y, int(bar_w * ratio), bar_h), border_radius=6)
        text_target = game.font.render(f"Target: {game.target.lives}/{game.max_target_lives}", True, WHITE)
        game.screen.blit(text_target, (x_bar, BAR_Y - 22))
