import pygame

from ui.button import Button
from jogo.systems.skins import load_skin, listar_skins
import math
import os
from jogo.states.tela_pre_game.pre_game import PreGame


class TelaSkins:

    val=0

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # BACKGROUND
        self.background = pygame.image.load(
            "assets/images/menu/lobby.png"
        )

        self.background = pygame.transform.scale(
            self.background,
            (self.width, self.height)
        )

        # OVERLAY
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(60)
        self.overlay.fill((0, 0, 0))

        # FONTE
        self.font = pygame.font.SysFont(
            "times new roman",
            54,
            bold=True
        )

        # TÍTULO
        self.title = self.font.render(
            "SKINS",
            True,
            (230, 210, 160)
        )

        self.title_rect = self.title.get_rect(
            center=(self.width // 2, 60)
        )

        # BOTÃO VOLTAR
        self.back_button = Button(
            "←",
            40,
            35,
            90,
            70,
            font_size=52
        )

    def draw(self, screen):

        # FUNDO
        screen.blit(self.background, (0, 0))

        # OVERLAY
        screen.blit(self.overlay, (0, 0))

        # TÍTULO
        screen.blit(self.title, self.title_rect)

        # BOTÃO
        self.back_button.draw(screen)

        self.skins_caminho = "assets/skins"

        self.thumbs_skins = {}
        for pasta in os.listdir(self.skins_caminho):
            caminho_thumb = f"{self.skins_caminho}/{pasta}/cabeca.png"
            if os.path.exists(caminho_thumb):
                img = pygame.image.load(caminho_thumb).convert_alpha()
                # Redimensiona para um tamanho de ícone (ex: 60x60)
                self.thumbs_skins[pasta] = pygame.transform.scale(img, (60, 60))

        fundo_skins = pygame.Rect(self.width//2 - 500, self.height//2 - 200, 500, 400)

        pygame.draw.rect(screen, (230, 230, 230), fundo_skins)

        for i, nome_skin in enumerate(os.listdir(self.skins_caminho)):
            # Somamos +1 no índice para não ocupar o lugar do botão Debug
            self.indice_ajustado = i 
            self.coluna = self.indice_ajustado % 4
            self.linha = self.indice_ajustado // 4
            x = fundo_skins.x + 10 + (self.coluna * 110)
            y = fundo_skins.y + 50 + (self.linha * 110)
            Button(f"{i}", x, y, 100, 100).draw(screen)

            
            if nome_skin in self.thumbs_skins:
                screen.blit(self.thumbs_skins[nome_skin], (x + 20, y + 20))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.botao=1
                else:                    
                    self.botao=0
            if Button(f"{i}", x, y, 100, 100).handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=pygame.mouse.get_pos(), button=self.botao)):
                print(f"Skin {nome_skin} selecionada!")
                self.val=i
                
            #if Button.handle_event(self, event):
            #    carregar_skin_pasta(nome_skin)


               
        # PREVIEW
        self.preview_rect = pygame.Rect(self.width // 2 + 50, 170, 500, 320)

        self.skins = listar_skins()

        self.current_skin = self.val

        if len(self.skins) > 0:
            self.loaded_skin = load_skin(
                self.skins[self.current_skin]
            )
        else:
            self.loaded_skin = None

        # texto preview
        self.preview_text = self.font.render("PERSONAGEM", True, (230, 210, 160))
        self.preview_rect_text = self.preview_text.get_rect(
            center = (self.preview_rect.centerx, self.preview_rect.y + 40))
         # preview personagem
        pygame.draw.rect(screen, (55, 55, 65), self.preview_rect, border_radius = 22)
        preview_glow = pygame.Surface((500, 320), pygame.SRCALPHA)

        pygame.draw.rect(preview_glow, (255, 220, 120, 25), (0, 0, 500, 320), border_radius = 22)
        
        screen.blit(preview_glow, self.preview_rect.topleft)

        pygame.draw.rect(screen, (212, 175, 55), self.preview_rect, width = 3, border_radius = 22)

        # texto preview
        screen.blit(self.preview_text, self.preview_rect_text)
        # personagem
        if self.loaded_skin:

            # animação idle
            offset = math.sin(pygame.time.get_ticks() * 0.005) * 5

            # cabeça
            head = pygame.transform.scale(self.loaded_skin["cabeca"], (90, 90))

            # corpo
            body = pygame.transform.scale(self.loaded_skin["torco"], (120, 140))

            # sombra
            shadow_surface = pygame.Surface((160, 40), pygame.SRCALPHA)

            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, 160, 40))

            screen.blit(shadow_surface, (self.preview_rect.centerx - 80, self.preview_rect.bottom - 70))

            # desenhar tronco
            screen.blit(body, (self.preview_rect.centerx - 60, self.preview_rect.centery - 20 + offset))

            # desenhar cabeça
            screen.blit(head, (self.preview_rect.centerx - 45, self.preview_rect.centery - 100 + offset))