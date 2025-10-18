import pygame
from credits import show_credits
from settings import WIDTH, HEIGHT
from game_action import Game
from instructions import show_instructions


class Menu:
    def __init__(self):
        pygame.init()

        self.font = pygame.font.SysFont("Lucida Sans Typewriter", 40)

        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Crazy Mommy — Menu")

        try:
            self.bg = pygame.image.load("assets/images/background/MenuBg.png").convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((30, 30, 60))

    # -----------------------------------------------------------------
    def run(self):
        """Loop principal do menu com som e navegação"""

        try:
            pygame.mixer.music.load("assets/sounds/menutheme.wav")
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f" Música do menu não encontrada: {e}")

        try:
            sound_move = pygame.mixer.Sound("assets/sounds/cursor-move.wav")
            sound_select = pygame.mixer.Sound("assets/sounds/selectenter.flac")
        except Exception as e:
            print(f"Alguns sons não foram carregados: {e}")
            sound_move = sound_select = None

        options = ["Jogar", "Instruções", "Créditos", "Sair"]
        selected = 0
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(options)
                        if sound_move: sound_move.play()

                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(options)
                        if sound_move: sound_move.play()

                    elif event.key == pygame.K_RETURN:
                        if sound_select: sound_select.play()

                        if selected == 0:
                            pygame.mixer.music.stop()
                            self.window.fill((0, 0, 0))
                            pygame.display.flip()
                            Game().run()
                            pygame.mixer.music.play(-1)

                        elif selected == 1:
                            show_instructions(self.window)
                            self.window.blit(self.bg, (0, 0))
                            pygame.display.flip()

                        elif selected == 2:
                            show_credits(self.window)
                            self.window.blit(self.bg, (0, 0))
                            pygame.display.flip()

                        elif selected == 3:
                            running = False

            self.window.blit(self.bg, (0, 0))
            self.menu_text("CRAZY MOMMY", (WIDTH // 2, 150), (255, 215, 0))

            for i, option in enumerate(options):
                color = (255, 215, 0) if i == selected else (245, 245, 245)
                self.menu_text(f"> {option} <", (WIDTH // 2, 300 + i * 60), color)

            pygame.display.flip()
            clock.tick(60)

        pygame.mixer.music.stop()
        pygame.quit()

    # -----------------------------------------------------------------
    def menu_text(self, text, pos, color=(255, 255, 255)):
        """Renderiza texto centralizado na tela"""
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(center=pos)
        self.window.blit(surface, rect)
