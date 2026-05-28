import pygame

from ui.button import Button
from jogo.systems.skins import load_skin
from jogo.systems.skins import listar_skins

class PreGame:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("arial", 60, bold=True)
        
        # fundo
        self.background = pygame.image.load("assets/images/menu/lobby.jpg")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        #overlay
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(40)
        self.overlay.fill((0, 0, 0))
        
        #botões
        self.preview_rect = pygame.Rect( width // 2 - 200, 120, 400, 250)
        self.back_button = Button("←", 30, 30, 60, 50)
        self.skin_button = Button("SKINS", 180, 500, 220, 60)
        self.mode_button = Button("MODO", 530, 500, 220, 60)
        self.scenario_button = Button("CENARIO", 880, 500, 220, 60)
        self.start_button = Button("INICIAR", width // 2 - 150, 610, 300, 70)
        self.config_button = Button("⚙", width - 100, height - 100, 60, 60)
        self.selected_mode = "AFK"
        self.skins = [ "teste", "testemult"]
        self.current_skin = 0
        self.skins = listar_skins()
        print(self.skins)
        self.current_skin = 0

        if len(self.skins) > 0:
            self.loaded_skin = load_skin(self.skins[self.current_skin])
        else:
            self.loaded_skin = None
                    
    def draw(self, screen):

        screen.fill((0, 0, 0))

        # fundo
        screen.blit(self.background, (0, 0))

        # overlay
        screen.blit(self.overlay, (0, 0))

        # preview personagem
        pygame.draw.rect(screen, (80, 80, 90), self.preview_rect, border_radius=20)
        pygame.draw.rect(screen, (180, 180, 180), self.preview_rect, width=3, border_radius=20)

        # texto preview
        preview_text = self.font.render("PREVIEW", True, (255, 255, 255))
        screen.blit(preview_text, (self.preview_rect.x + 85, self.preview_rect.y + 90))
        
        if self.loaded_skin:
            head = pygame.transform.scale(self.loaded_skin["cabeca"], (90, 90))
            body = pygame.transform.scale(self.loaded_skin["torco"], (120, 140))
            
            screen.blit(body, (self.preview_rect.centerx - 60, self.preview_rect.centery - 20))
            screen.blit(head, (self.preview_rect.centerx - 45, self.preview_rect.centery - 100))

        # desenhar tronco
        screen.blit(body, (self.preview_rect.centerx - 60, self.preview_rect.centery - 20))

        # desenhar cabeça
        screen.blit(head, (self.preview_rect.centerx - 45, self.preview_rect.centery - 100))
        
        self.mode_button.text = f"MODO: {self.selected_mode}"

        # desenhar botões
        self.back_button.draw(screen)
        self.skin_button.text = f"SKIN: {self.skins[self.current_skin]}"
        self.skin_button.draw(screen)
        self.mode_button.draw(screen)
        self.scenario_button.draw(screen)
        self.start_button.draw(screen)
        self.config_button.draw(screen)