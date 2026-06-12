import pygame
import os

def load_sprites(caminho):
    sprites = {}
    for arquivo in os.listdir(caminho):
        if arquivo.endswith(".png"):
            nome = os.path.splitext(arquivo)[0]
            img = pygame.image.load(os.path.join(caminho, arquivo)).convert_alpha()
            sprites[nome] = img
    return sprites