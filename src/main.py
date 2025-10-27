import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from src.menu import Menu


def main():
    try:
        Menu().run()
    except Exception as e:
        print(f"Erro ao iniciar o jogo: {e}")
    finally:
        import pygame
        pygame.quit()


if __name__ == "__main__":
    main()
