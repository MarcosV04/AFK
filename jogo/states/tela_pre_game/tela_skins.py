import pygame
import math
import os
from ui.button import Button
from jogo.systems.skins import load_skin, listar_skins

class TelaSkins:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.val = 0
        self.skins_caminho = "assets/skins"
        
        self.skins = listar_skins()
        # Salva o nome em texto em vez de só o número! É 100% à prova de bugs:
        self.skin_selecionada_nome = self.skins[0] if self.skins else "padrao"

        self.background = pygame.transform.scale(
            pygame.image.load("assets/images/menu/lobby.png").convert(),
            (self.width, self.height)
        )

        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(60)
        self.overlay.fill((0, 0, 0))

        self.font = pygame.font.SysFont("times new roman", 54, bold=True)
        self.title = self.font.render("SKINS", True, (230, 210, 160))
        self.title_rect = self.title.get_rect(center=(self.width // 2, 60))

        self.back_button = Button("←", 40, 35, 90, 70, font_size=52)

        self.thumbs_skins = {}
        self.botoes_skins = []
        self.fundo_skins_rect = pygame.transform.scale(
            pygame.image.load("assets/images/menu/beckmenu.png").convert(),
            (500, 400)
        )
        self.fundo_skins_rect_coordenada = (self.width // 2 - 500, self.height // 2 - 200)
        
        self._carregar_thumbnails_e_botoes()

        self.head_preview = None
        self.body_preview = None
        self._atualizar_preview()

        self.shadow_surface = pygame.Surface((160, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(self.shadow_surface, (0, 0, 0, 100), (0, 0, 160, 40))

    def _carregar_thumbnails_e_botoes(self):
        lista_pastas = sorted(os.listdir(self.skins_caminho)) # sorted garante a mesma ordem sempre!
        
        for i, nome_skin in enumerate(lista_pastas):
            caminho_thumb = f"{self.skins_caminho}/{nome_skin}/cabeca.png"
            if os.path.exists(caminho_thumb):
                img = pygame.image.load(caminho_thumb).convert_alpha()
                self.thumbs_skins[nome_skin] = pygame.transform.scale(img, (60, 60))

            coluna = i % 4
            linha = i // 4
            x = self.fundo_skins_rect_coordenada[0] + 10 + (coluna * 110)
            y = self.fundo_skins_rect_coordenada[1] + 50 + (linha * 110)
            
            botao = Button(f"{i}", x, y, 100, 100, font_size=16)
            self.botoes_skins.append({"botao": botao, "nome": nome_skin, "indice": i})

    def _atualizar_preview(self):
        if len(self.skins) > 0:
            loaded_skin = load_skin(self.skin_selecionada_nome)
            self.head_preview = pygame.transform.scale(loaded_skin["cabeca"], (90, 90))
            self.body_preview = pygame.transform.scale(loaded_skin["torco"], (120, 140))

    # --- A PONTE COM O MAESTRO ---
    def handle_events(self, event):
        if self.back_button.handle_event(event):
            return True # Avisa o GameManager: "Pode voltar pro lobby"

        for item in self.botoes_skins:
            if item["botao"].handle_event(event):
                self.val = item["indice"]
                self.skin_selecionada_nome = item["nome"]
                print(f"Skin selecionada: {self.skin_selecionada_nome}")
                self._atualizar_preview()

        return False

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay, (0, 0))
        screen.blit(self.title, self.title_rect)
        self.back_button.draw(screen)

        screen.blit(self.fundo_skins_rect, self.fundo_skins_rect_coordenada)

        for item in self.botoes_skins:
            botao = item["botao"]
            botao.draw(screen)
            if item["nome"] in self.thumbs_skins:
                screen.blit(self.thumbs_skins[item["nome"]], (botao.rect.x + 20, botao.rect.y + 20))

        preview_rect = pygame.Rect(self.width // 2 + 50, self.height // 2 - 160, 500, 320)
        pygame.draw.rect(screen, (55, 55, 65), preview_rect, border_radius=22)
        pygame.draw.rect(screen, (212, 175, 55), preview_rect, width=3, border_radius=22)

        preview_text = self.font.render("PERSONAGEM", True, (230, 210, 160))
        screen.blit(preview_text, preview_text.get_rect(center=(preview_rect.centerx, preview_rect.y + 40)))

        if self.head_preview and self.body_preview:
            offset = math.sin(pygame.time.get_ticks() * 0.005) * 5
            screen.blit(self.shadow_surface, (preview_rect.centerx - 80, preview_rect.bottom - 70))
            screen.blit(self.body_preview, (preview_rect.centerx - 60, preview_rect.centery - 20 + offset))
            screen.blit(self.head_preview, (preview_rect.centerx - 45, preview_rect.centery - 100 + offset))