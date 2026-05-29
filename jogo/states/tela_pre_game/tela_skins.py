import pygame

from ui.button import Button


class TelaSkins:

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