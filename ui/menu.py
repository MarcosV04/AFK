import pygame

def desenhar_menu(tela, fonte, rect_abrir_menu, menu_aberto, largura):

    # BOTÃO MENU
    pygame.draw.rect(tela, (150, 150, 150), rect_abrir_menu)

    tela.blit(
        fonte.render( "ABRIR MENU", True, (255, 255, 255)), (largura - 140, 20))

    # MENU ABERTO
    if menu_aberto:

        fundo_menu = pygame.Rect(largura - 260, 60, 250, 300)

        pygame.draw.rect(tela, (40, 40, 40), fundo_menu)

        pygame.draw.rect(tela, (255, 255, 255), fundo_menu, 2)

        texto = fonte.render("MENU ABERTO", True, (255, 255, 255))

        tela.blit(texto, (largura - 220, 80))