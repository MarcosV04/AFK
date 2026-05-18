import pygame
import pymunk
import pymunk.pygame_util
import math
import os


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

    rodando = True

    # SPRITES
    sprites_boneco = {}

    skins_disponiveis = (os.listdir("skins")
                         
        if os.path.exists("skins")
        else [])

    thumbs_skins = {}

    # FUNÇÕES AUXILIARES
    def criar_chao():

        chao = pymunk.Segment(espaco.static_body, (0, ALTURA - 50), (LARGURA, ALTURA - 50), 5)

        chao.friction = 1.0

        espaco.add(chao)

    def criar_bloco(x, y, largura, altura, massa=10):

        momento = pymunk.moment_for_box(massa, (largura, altura))

        corpo = pymunk.Body(massa, momento)

        corpo.position = x, y

        forma = pymunk.Poly.create_box(corpo, (largura, altura))

        forma.friction = 0.5
        forma.elasticity = 0.3

        espaco.add(corpo, forma)

        return forma

    def criar_corda(corpo_a, corpo_b, ancora_a, ancora_b, comprimento):

        corda = pymunk.SlideJoint(corpo_a, corpo_b, ancora_a, ancora_b, 0, comprimento)

        espaco.add(corda)

        return corda

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

    # BONECO
    def criar_boneco():
        torco = criar_bloco(LARGURA // 2, 200, 75, 90)
        cabeca = criar_bloco(LARGURA // 2, 90, 80, 80)
        bresq = criar_bloco(LARGURA // 2 - 50, 200, 25, 50)
        antesq = criar_bloco(LARGURA // 2 - 50, 275, 25, 50)
        bradir = criar_bloco(LARGURA // 2 + 50, 200, 25, 50)
        antdir = criar_bloco(LARGURA // 2 + 50, 275, 25, 50)
        peresq = criar_bloco(LARGURA // 2 - 25, 325, 25, 50)
        panesq = criar_bloco(LARGURA // 2 - 25, 400, 25, 50)
        perdir = criar_bloco(LARGURA // 2 + 25, 325, 25, 50)
        pandir = criar_bloco(LARGURA // 2 + 25, 400, 25, 50)
        cintura = criar_bloco(LARGURA // 2, 250, 75, 35)

        # CORDAS
        criar_corda(torco.body, cabeca.body, (0, -45), (0, 40), 25)
        criar_corda(torco.body, bresq.body, (-37.5, -30), (0, -25), 20)
        criar_corda(bresq.body, antesq.body, (0, 25), (0, -25), 25)
        criar_corda(torco.body, bradir.body, (37.5, -30), (0, -25), 20)
        criar_corda(bradir.body, antdir.body, (0, 25), (0, -25), 25)
        criar_corda(torco.body, cintura.body, (0, 45), (0, -17.5), 25)
        criar_corda(cintura.body, peresq.body, (-25, 17.5), (0, -25), 25)
        criar_corda(peresq.body, panesq.body, (0, 25), (0, -25), 25)
        criar_corda(cintura.body, perdir.body, (25, 17.5), (0, -25), 25)
        criar_corda(perdir.body, pandir.body, (0, 25), (0, -25), 25)

        # Corda
        criar_corda(pontos_controle[2], cabeca.body, (0, 0), (0, -40), 100)
        criar_corda(pontos_controle[0], antesq.body, (0, 0), (0, 25), 150)
        criar_corda(pontos_controle[4], antdir.body, (0, 0), (0, 25), 150)
        criar_corda(pontos_controle[1], peresq.body, (0, 0), (0, 25), 400)
        criar_corda(pontos_controle[3], perdir.body, (0, 0), (0, 25), 400)

        return{
            "cabeca": cabeca,
            "torco": torco,
            "bresq": bresq,
            "antesq": antesq,
            "bradir": bradir,
            "antdir": antdir,
            "peresq": peresq,
            "panesq": panesq,
            "perdir": perdir,
            "pandir": pandir,
            "cintura": cintura
        }

    # SKINS
    def carregar_skin_pasta(nome_pasta):

        nonlocal sprites_boneco

        caminho = f"skins/{nome_pasta}"

        tamanhos = {
            "cabeca": (80, 80),
            "torco": (75, 90),
            "bresq": (25, 50),
            "antesq": (25, 50),
            "bradir": (25, 50),
            "antdir": (25, 50),
            "peresq": (25, 50),
            "panesq": (25, 50),
            "perdir": (25, 50),
            "pandir": (25, 50),
            "cintura": (75, 35)
        }

        sprites_boneco = {}

        for parte, tamanho in tamanhos.items():

            arquivo = f"{caminho}/{parte}.png"

            if os.path.exists(arquivo):

                img = pygame.image.load(arquivo).convert_alpha()

                sprites_boneco[parte] = pygame.transform.scale(img, tamanho)

    def carregar_thumbs():

        for pasta in skins_disponiveis:

            caminho = f"skins/{pasta}/cabeca.png"

            if os.path.exists(caminho):

                img = pygame.image.load(caminho).convert_alpha()

                thumbs_skins[pasta] = pygame.transform.scale(img, (60, 60))

    # CENÁRIO
    criar_chao()
    meu_boneco = criar_boneco()
    
    carregar_thumbs()
    criar_bloco(
        LARGURA // 2 + 200, 100, 20, 100, 50)

    # MOUSE
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

    # LOOP PRINCIPAL
    while rodando:

        tela.fill((240, 240, 240))

        mouse_pos = pygame.mouse.get_pos()

        # CAMERA
        if fila is not None and not fila.empty():

            try:

                while not fila.empty():
                    pontos = fila.get_nowait()

                if not modo_edicao and pontos and len(pontos) >= 21:

                    escala_x = 2
                    escala_y = 1.5

                    pontos_controle[0].position = (pontos[4][0] * escala_x, pontos[4][1] * escala_y)
                    pontos_controle[1].position = (pontos[8][0] * escala_x, pontos[8][1] * escala_y)
                    pontos_controle[2].position = (pontos[12][0] * escala_x, pontos[12][1] * escala_y)
                    pontos_controle[3].position = (pontos[16][0] * escala_x, pontos[16][1] * escala_y)
                    pontos_controle[4].position = (pontos[20][0] * escala_x, pontos[20][1] * escala_y)


            except Exception as erro:
                print("Erro camera:", erro)

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
        pygame.draw.rect(tela, (150, 150, 150), rect_abrir_menu)

        tela.blit(
            fonte.render("ABRIR MENU", True, (255, 255, 255)), (LARGURA - 140, 20))

        # MENU ABERTO
        if menu_aberto:

            fundo_menu = pygame.Rect(LARGURA - 260, 60, 250, 300)

            pygame.draw.rect(tela, (40, 40, 40), fundo_menu)

            pygame.draw.rect(tela, (255, 255, 255), fundo_menu, 2)

            texto = fonte.render("MENU ABERTO", True, (255, 255, 255))

            tela.blit(texto, (LARGURA - 220, 80))
        
        # CURSOR CAMERA
        pygame.display.flip()

        relogio.tick(60)

    pygame.quit()

    if config is not None:
        config.put("Fechar")