import pygame

from ui.button import Button


class MainMenu:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        # background
        self.background = pygame.image.load("assets/images/menu/lobby.jpg")

        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # overlay escuro
        self.overlay = pygame.Surface((self.width, self.height))
        self.overlay.set_alpha(40)
        self.overlay.fill((0, 0, 0))

        # configurações dos botões
        button_width = 400
        button_height = 70

        center_x = self.width // 2 - button_width // 2

        # botões
        self.play_button = Button("JOGAR", center_x, 300, button_width, button_height)

    def draw(self, screen):

        screen.fill((0, 0, 0))

        screen.blit(self.background, (0, 0))

        screen.blit(self.overlay, (0, 0))

        self.play_button.draw(screen)
        
        
