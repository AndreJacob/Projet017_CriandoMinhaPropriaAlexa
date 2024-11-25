import pygame

# Inicializa o mixer de áudio do pygame
pygame.mixer.init()

def play_audio(file_path):
    """Reproduz o arquivo de áudio fornecido."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
