import pygame

class Button:

    def __init__(self, text, x, y, width, height):

        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (120, 85, 40)
        self.hover_color = (160, 120, 60)
        self.font = pygame.font.SysFont("arial", 40, bold=True)

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect( screen, color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True

        return False