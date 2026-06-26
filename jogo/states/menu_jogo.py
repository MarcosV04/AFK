import pygame


def desenhar_menu(tela, fonte, rect_abrir_menu, menu_aberto, largura):

    # BOTÃO MENU
    pygame.draw.rect(tela, (150, 150, 150), rect_abrir_menu)
    tela.blit(fonte.render("ABRIR MENU", True, (255, 255, 255)), (largura - 140, 20))

    # MENU
    if menu_aberto:

        fundo = pygame.Rect(largura - 260, 60, 250, 180)
        pygame.draw.rect(tela, (40, 40, 40), fundo)
        pygame.draw.rect(tela, (255, 255, 255), fundo, 2)

        # CONTINUAR
        continuar = pygame.Rect(largura - 240, 110, 200, 40)
        pygame.draw.rect(tela, (80, 80, 80), continuar)

        tela.blit(fonte.render("Continuar", True, (255,255,255)), (largura - 205,118))

        # SAIR
        sair = pygame.Rect(largura - 240, 170, 200, 40)
        pygame.draw.rect(tela, (120,40,40), sair)

        tela.blit(fonte.render("Sair", True, (255,255,255)), (largura - 175,178))