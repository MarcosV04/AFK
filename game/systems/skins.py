import pygame
import os

def carregar_skin_pasta(nome_pasta):

    caminho = f"assets/skins/{nome_pasta}"

    tamanhos = {
        "cabeca": (80, 80),
        "torco": (75, 90),
        "bresq": (25, 50),
        "antesq": (25, 50),
        "bradir": (25, 50),
        "antdir": (25, 50),
        "peresq": (25, 50),
        "panesq": (25, 50),
        "perdir": (25, 50),
        "pandir": (25, 50),
        "cintura": (75, 35)
    }

    sprites_boneco = {}

    for parte, tamanho in tamanhos.items():

        arquivo = f"{caminho}/{parte}.png"

        if os.path.exists(arquivo):

            img = pygame.image.load(arquivo).convert_alpha()

            sprites_boneco[parte] = pygame.transform.scale(img, tamanho)

    return sprites_boneco


def carregar_thumbs(skins_disponiveis):

    thumbs_skins = {}

    for pasta in skins_disponiveis:

        caminho = f"assets/skins/{pasta}/cabeca.png"

        if os.path.exists(caminho):

            img = pygame.image.load(caminho).convert_alpha()

            thumbs_skins[pasta] = pygame.transform.scale(img, (60, 60))

    return thumbs_skins

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def load_skin(skin_name):

    skin_path = os.path.join("assets", "skins", skin_name)

    skin = {
        "cabeca": pygame.image.load(os.path.join(skin_path, "cabeca.png")).convert_alpha(),
        "torco": pygame.image.load(os.path.join(skin_path, "torco.png")).convert_alpha()
        }

    return skin

def listar_skins():

    caminho = "assets/skins"

    if not os.path.exists(caminho):
        return []

    return os.listdir(caminho)