import pygame

from ui.button import Button

class menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # BACKGROUND
        self.background = pygame.image.load("assets/images/menu/lobby.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # OVERLAY ESCURO
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(40)
        self.overlay.fill((0, 0, 0))

        # CONFIG BOTÃO
        button_width = 400
        button_height = 70
        center_x = (self.width // 2 - button_width // 2)

        # FONTE
        self.font = pygame.font.SysFont(None, 40)

        # BOTÃO PLAY
        #self.play_button = pygame.Rect(center_x, 300, button_width, button_height)
        self.play_button = Button("JOGAR", center_x, 420, 500, 120, font_size=56)

    def draw(self, screen):

        # FUNDO
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay, (0, 0))
        
        self.play_button.draw(screen)

    def handle_events(self, event):

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if self.play_button.handle_event(event):

                return True

        return False