import pygame

class menu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # BACKGROUND
        self.background = pygame.image.load("assets/images/menu/lobby.jpg")
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
        self.play_button = pygame.Rect(center_x, 300, button_width, button_height)

    def draw(self, screen):

        # FUNDO
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0, 0))
        screen.blit(self.overlay, (0, 0))

        # BOTÃO
        pygame.draw.rect(screen, (40, 40, 40), self.play_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.play_button, 3, border_radius=12)

        # TEXTO
        texto = self.font.render("JOGAR", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=self.play_button.center)
        screen.blit(texto, texto_rect)

    def handle_events(self, event):

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
            if self.play_button.collidepoint(event.pos):

                return True

        return False