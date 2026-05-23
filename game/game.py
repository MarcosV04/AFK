import pygame
import pymunk
import pymunk.pygame_util
import math
import os

from physics.world import criar_chao, criar_bloco
from characters.boneco import criar_boneco
from ui.menu import desenhar_menu
from camera.controle import atualizar_camera
from skins_system.skins import carregar_skin_pasta, carregar_thumbs

def jogo(fila, config, gestos):
    
    pygame.init()

    LARGURA, ALTURA = 1280, 720

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("🎭 AFK - Away From the Keyboard")

    relogio = pygame.time.Clock()
    
    fonte = pygame.font.SysFont(None, 24)

    # FÍSICA
    espaco = pymunk.Space()
    espaco.gravity = (0, 981)

    opcoes_desenho = pymunk.pygame_util.DrawOptions(tela)
     
    # ESTADOS
    mostrar_debug = False
    menu_aberto = False
    janela_skins_aberta = False

    conexao_garra = None
    ponto_arrastando = None
    mouse_joint = None
    modo_edicao = False

    rodando = True

    # SPRITES
    sprites_boneco = carregar_skin_pasta("teste")

    skins_disponiveis = (os.listdir("skins")
                         
        if os.path.exists("skins")
        else [])

    thumbs_skins = {}

    # PONTOS CONTROLE
    
    pontos_controle = []

    for i in range(5):

        corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        corpo.position = ((LARGURA // 2) - 200 + (i * 100), 150)

        forma = pymunk.Circle(corpo, 15)

        forma.sensor = True
        
        forma.collision_type = 1

        espaco.add(corpo, forma)

        pontos_controle.append(corpo)

    # CENÁRIO
    criar_chao(espaco, LARGURA, ALTURA)

    meu_boneco = criar_boneco(espaco, pontos_controle, LARGURA)
    
    thumbs_skins = carregar_thumbs(skins_disponiveis)
    
    criar_bloco(espaco, LARGURA  // 2 + 200, 100, 20, 100, 50)

    # MOUSE
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    # LOOP PRINCIPAL
    while rodando:

        tela.fill((240, 240, 240))

        mouse_pos = pygame.mouse.get_pos()
        
        atualizar_camera(fila, pontos_controle, modo_edicao)

        # GESTOS
        acao = "Parado"

        if gestos is not None and not gestos.empty():

            try:
                acao = gestos.get_nowait()
                
            except Exception as erro:
                print("ERRO:", erro)

        sinal_ativo = (acao == "Agachar")

        # MENU
        rect_abrir_menu = pygame.Rect(LARGURA - 150, 10, 140, 40)

        # EVENTOS
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.KEYDOWN:
            
                if evento.key == pygame.K_h:
                    modo_edicao = not modo_edicao
                    print("Modo edição:", modo_edicao)
                    
                    mostrar_debug = not mostrar_debug

            elif evento.type == pygame.MOUSEBUTTONDOWN:
    
                if evento.button == 1:
                
                    # MENU
                    if rect_abrir_menu.collidepoint(mouse_pos):
                    
                        print("Funciona o menu")

                        menu_aberto = not menu_aberto

                    else:
                    
                        # OBJETOS FÍSICOS
                        info = espaco.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())

                        if info and info.shape:
                        
                            corpo = info.shape.body

                            # PONTOS AZUIS
                            if corpo in pontos_controle:
                            
                                ponto_arrastando = corpo

                            # OBJETOS DINÂMICOS
                            elif corpo.body_type == pymunk.Body.DYNAMIC:
                            
                                if mouse_joint is None:
                                
                                    mouse_body.position = mouse_pos

                                    mouse_joint = pymunk.PivotJoint(mouse_body, corpo, mouse_pos)

                                    mouse_joint.max_force = 250000

                                    espaco.add(mouse_joint)
                    
            elif evento.type == pygame.MOUSEBUTTONUP:
            
                if evento.button == 1:
                    
                    ponto_arrastando = None
                    modo_edicao = False
                
                    if mouse_joint:
                    
                        espaco.remove(mouse_joint)
            
                        mouse_joint = None

        # MOVIMENTO
        if ponto_arrastando is not None:
            ponto_arrastando.position = mouse_pos

        if mouse_joint:
            mouse_body.position = mouse_pos

        # GARRA
        braco_dir = meu_boneco["antdir"]

        pos_mao = braco_dir.body.local_to_world((0, 25))

        raio = 40

        if sinal_ativo:

            pygame.draw.circle(tela, (0, 255, 0), (int(pos_mao.x), int(pos_mao.y)), raio, 2)

            if conexao_garra is None:

                info = espaco.point_query_nearest(pos_mao, raio, pymunk.ShapeFilter())

                if (info and info.shape.body.body_type == pymunk.Body.DYNAMIC and info.shape.body != braco_dir.body):

                    conexao_garra = pymunk.PivotJoint(braco_dir.body, info.shape.body, pos_mao)

                    conexao_garra.max_force = 500000

                    espaco.add(conexao_garra)

        else:

            if conexao_garra:

                espaco.remove(conexao_garra)

                conexao_garra = None

        # FÍSICA
        espaco.step(1 / 60)

        # DESENHO
        pygame.draw.line(tela, (50, 50, 50), (0, ALTURA - 50), (LARGURA, ALTURA - 50), 5)

        # CORDAS
        for conexao in espaco.constraints:

            if conexao == conexao_garra:
                continue

            pos_a = conexao.a.local_to_world(conexao.anchor_a)

            pos_b = conexao.b.local_to_world(conexao.anchor_b)

            pygame.draw.line(tela, (70, 40, 20), pos_a, pos_b, 2)

        # DEBUG
        if mostrar_debug:

            espaco.debug_draw(opcoes_desenho)

        else:

            if sprites_boneco:

                for nome, img in sprites_boneco.items():

                    forma = meu_boneco[nome]

                    corpo = forma.body

                    img_rot = pygame.transform.rotate(img, -math.degrees(corpo.angle))

                    rect = img_rot.get_rect(center=corpo.position)

                    tela.blit(img_rot, rect)

            else:

                espaco.debug_draw(opcoes_desenho)

        # PONTOS CONTROLE
        for p in pontos_controle:

            pygame.draw.circle(tela, (0, 100, 255), (int(p.position.x), int(p.position.y)), 15, 2)

        # MENU
        desenhar_menu(tela, fonte, rect_abrir_menu, menu_aberto, LARGURA)
        
        # CURSOR CAMERA
        pygame.display.flip()

        relogio.tick(60)

    pygame.quit()

    if config is not None:
        config.put("Fechar")