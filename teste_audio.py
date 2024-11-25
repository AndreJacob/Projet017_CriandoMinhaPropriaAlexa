import pygame

# Inicializa o mixer de áudio do pygame
pygame.mixer.init()

# Carrega o arquivo MP3
pygame.mixer.music.load("queBurro.mp3")  # Substitua pelo nome do seu arquivo MP3

# Reproduz o áudio
pygame.mixer.music.play()

# Aguarda até que o áudio termine
while pygame.mixer.music.get_busy(): 
    pygame.time.Clock().tick(10)
