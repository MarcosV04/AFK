import math
import pygame

from ui.button import Button
from jogo.systems.skins import load_skin
from jogo.systems.skins import listar_skins


class PreGame:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # fonte
        self.font = pygame.font.SysFont("times new roman", 42, bold = True)

        # fundo
        self.background = pygame.image.load("assets/images/menu/lobby.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # overlay
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(55)
        self.overlay.fill((0, 0, 0))

        # botões
        self.back_button = Button("←", 40, 35, 90, 70, font_size = 52)

        #self.skin_button = Button("Skins", 90, 520, 300, 90, font_size = 36)

        #self.mode_button = Button("Modo", width // 2 - 150, 520, 300, 90, font_size = 36)

        #self.scenario_button = Button( "Cenário", width - 390, 520, 300, 90, font_size = 36)
        
        button_width = 260
        button_height = 85
        button_spacing = 60
        button_y = 438
        
        total_width = ((button_width * 3) + (button_spacing * 2))
        
        start_x = (width - total_width) // 2
        
        
        self.skin_button = Button("Skins", start_x, button_y, button_width, button_height, font_size = 36)
        
        self.mode_button = Button("Modo", start_x + button_width + button_spacing, button_y, button_width, button_height, font_size = 36)
        
        self.scenario_button = Button("Cenário", start_x + (button_width + button_spacing) * 2, button_y, button_width, button_height, font_size = 36)

        self.start_button = Button("Iniciar", width // 2 - 220, 293, 440, 100, font_size = 52)

        self.config_button = Button("⚙", width - 110, height - 100, 70, 70, font_size = 36)

        self.skins = listar_skins()
        self.current_skin = 0

        print(self.skins)

        # PREVIEW
        #self.preview_rect = pygame.Rect( width // 2 - 250, 100, 500, 320)
#
        #if len(self.skins) > 0:
        #    self.loaded_skin = load_skin(
        #        self.skins[self.current_skin]
        #    )
        #else:
        #    self.loaded_skin = None
#
        ## texto preview
        #self.preview_text = self.font.render("PERSONAGEM", True, (230, 210, 160))
        #self.preview_rect_text = self.preview_text.get_rect(
        #    center = (self.preview_rect.centerx, self.preview_rect.y + 40))

    def draw(self, screen):

        screen.fill((0, 0, 0))

        # fundo
        screen.blit(self.background, (0, 0))

        # overlay
        screen.blit(self.overlay, (0, 0))

        # preview personagem
        #pygame.draw.rect(screen, (55, 55, 65), self.preview_rect, border_radius = 22)
        #preview_glow = pygame.Surface((500, 320), pygame.SRCALPHA)
#
        #pygame.draw.rect(preview_glow, (255, 220, 120, 25), (0, 0, 500, 320), border_radius = 22)
        #
        #screen.blit(preview_glow, self.preview_rect.topleft)
#
        #pygame.draw.rect(screen, (212, 175, 55), self.preview_rect, width = 3, border_radius = 22)
#
        ## texto preview
        #screen.blit(self.preview_text, self.preview_rect_text)

        # personagem
        #if self.loaded_skin:
#
        #    # animação idle
        #    offset = math.sin(pygame.time.get_ticks() * 0.005) * 5
#
        #    # cabeça
        #    head = pygame.transform.scale(self.loaded_skin["cabeca"], (90, 90))
#
        #    # corpo
        #    body = pygame.transform.scale(self.loaded_skin["torco"], (120, 140))
#
        #    # sombra
        #    shadow_surface = pygame.Surface((160, 40), pygame.SRCALPHA)
#
        #    pygame.draw.ellipse(shadow_surface, (0, 0, 0, 100), (0, 0, 160, 40))
#
        #    screen.blit(shadow_surface, (self.preview_rect.centerx - 80, self.preview_rect.bottom - 70))
#
        #    # desenhar tronco
        #    screen.blit(body, (self.preview_rect.centerx - 60, self.preview_rect.centery - 20 + offset))
#
        #    # desenhar cabeça
        #    screen.blit(head, (self.preview_rect.centerx - 45, self.preview_rect.centery - 100 + offset))
#


        # desenhar botões
        self.back_button.draw(screen)

        if len(self.skins) > 0:
            self.skin_button.text = f"{self.skins[self.current_skin]}"

        else:
            self.skin_button.text = "Sem skins"

        self.skin_button.draw(screen)
        self.scenario_button.draw(screen)
        self.start_button.draw(screen)
        self.config_button.draw(screen)