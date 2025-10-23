import os
import sys

def resource_path(relative_path):
    """Ajusta caminho para recursos (sons, imagens, etc.) compatível com PyInstaller."""
    try:
        base_path = sys._MEIPASS  # usado pelo PyInstaller
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
