import pygame
import pymunk
import pymunk.pygame_util
import math
def jogo():
    # --- Configurações Iniciais ---
    pygame.init()
    LARGURA, ALTURA = 1280, 720
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("🎭 AFK - Away From the Keyboard")
    relogio = pygame.time.Clock()

    # --- Configuração da Física (Pymunk) ---
    espaco = pymunk.Space()
    espaco.gravity = (0, 981) 
    opcoes_desenho = pymunk.pygame_util.DrawOptions(tela)

    # --- Funções para criar objetos ---
    def criar_chao(espaco):
        chao_body = espaco.static_body 
        chao_shape = pymunk.Segment(chao_body, (0, ALTURA - 50), (LARGURA, ALTURA - 50), 5)
        chao_shape.friction = 1.0
        espaco.add(chao_shape)

    def criar_bloco(espaco, x, y, largura, altura, massa=10):
        momento = pymunk.moment_for_box(massa, (largura, altura))
        corpo = pymunk.Body(massa, momento)
        corpo.position = x, y
        forma = pymunk.Poly.create_box(corpo, (largura, altura))
        forma.friction = 0.5
        forma.elasticity = 0.3
        espaco.add(corpo, forma)
        return forma

    def criar_esfera(espaco, x, y, raio, massa=10):
        momento = pymunk.moment_for_circle(massa, 0, raio, (0, 0))
        corpo = pymunk.Body(massa, momento)
        corpo.position = x, y
        forma = pymunk.Circle(corpo, raio)
        forma.friction = 0.5
        forma.elasticity = 0.3
        espaco.add(corpo, forma)
        return forma

    def criar_corda(espaco, corpo_a, corpo_b, ancora_a, ancora_b, comprimento):
        corda = pymunk.SlideJoint(corpo_a, corpo_b, ancora_a, ancora_b, 0, comprimento)
        espaco.add(corda)
        return corda

    # --- NOVO: Criando os 5 Pontos de Controle (Cinemáticos) ---
    pontos_controle = []
    for i in range(5):
        # Body_type KINEMATIC faz com que ignore gravidade e forças
        corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        corpo.position = ((LARGURA // 2) - 200 + (i * 100), 150)
        forma = pymunk.Circle(corpo, 15)
        forma.color = (0, 100, 255, 255) # Azul para identificar
        forma.sensor = True # Para não "atropelar" os blocos fisicamente se você não quiser
        espaco.add(corpo, forma)
        pontos_controle.append(corpo)

    # Criar o cenário e boneco
    criar_chao(espaco)
    def criar_boneco():
        torco = criar_bloco(espaco, LARGURA // 2, 200, 75, 90)
        cabeca = criar_bloco(espaco, LARGURA // 2 , 90, 80, 80)
        bresq = criar_bloco(espaco, LARGURA // 2 - 50, 200, 25, 50) 
        antesq = criar_bloco(espaco, LARGURA // 2 - 50, 275, 25, 50)
        bradir = criar_bloco(espaco, LARGURA // 2 + 50, 200, 25, 50) 
        antdir = criar_bloco(espaco, LARGURA // 2 + 50, 275, 25, 50)
        peresq = criar_bloco(espaco, LARGURA // 2 - 25, 325, 25, 50) 
        panesq = criar_bloco(espaco, LARGURA // 2 - 25, 400, 25, 50)
        perdir = criar_bloco(espaco, LARGURA // 2 + 25, 325, 25, 50) 
        pandir = criar_bloco(espaco, LARGURA // 2 + 25, 400, 25, 50)
        cintura = criar_bloco(espaco, LARGURA // 2, 250, 75, 35)
        criar_corda(espaco, torco.body, cabeca.body, (0, -45), (0, 40), 25)
        criar_corda(espaco, torco.body, bresq.body, (-37.5, -30), (0, -25), 20)
        criar_corda(espaco, bresq.body, antesq.body, (0, 25), (0, -25), 25)
        criar_corda(espaco, torco.body, bradir.body, (37.5, -30), (0, -25), 20)
        criar_corda(espaco, bradir.body, antdir.body, (0, 25), (0, -25), 25)
        criar_corda(espaco, torco.body, cintura.body, (0, 45), (0, -17.5), 25)
        criar_corda(espaco, cintura.body, peresq.body, (-25, 17.5), (0, -25), 25)
        criar_corda(espaco, peresq.body, panesq.body, (0, 25), (0, -25), 25)
        criar_corda(espaco, cintura.body, perdir.body, (25, 17.5), (0, -25), 25)
        criar_corda(espaco, perdir.body, pandir.body, (0, 25), (0, -25), 25)
        criar_corda(espaco, pontos_controle[2], cabeca.body, (0, 0), (0, -40), 100)
        criar_corda(espaco, pontos_controle[0], antesq.body, (0, 0), (0, 25), 300)
        criar_corda(espaco, pontos_controle[4], antdir.body, (0, 0), (0, 25), 300)
        criar_corda(espaco, pontos_controle[1], peresq.body, (0, 0), (0, 25), 450)
        criar_corda(espaco, pontos_controle[3], perdir.body, (0, 0), (0, 25), 450)
    criar_boneco()
    #criar_esfera(espaco, LARGURA // 2 + 200, 100, 50, 100) # Bola para interagir
    criar_bloco(espaco, LARGURA // 2 + 200, 100, 20, 100, 50) # Bloco para interagir

    # Variáveis para interação com o mouse
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    mouse_joint = None

    # Variáveis para criação da corda
    corpo_corda_a = None
    ancora_a_local = None

    # Variáveis de interação
    mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    mouse_joint = None
    ponto_arrastando = None # Armazena qual ponto azul estamos movendo

    rodando = True
    while rodando:
        tela.fill((240, 240, 240)) # Fundo cinza claro
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            # --- PEGAR BLOCOS COM O MOUSE ---
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    info = espaco.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())
                    if info and info.shape:
                        corpo_clicado = info.shape.body
                        # Se for um dos nossos pontos azuis (Kinematic)
                        if corpo_clicado in pontos_controle:
                            ponto_arrastando = corpo_clicado
                        # Se for um bloco normal (Dynamic)
                        elif corpo_clicado.body_type == pymunk.Body.DYNAMIC:
                            mouse_body.position = mouse_pos
                            mouse_joint = pymunk.PivotJoint(mouse_body, corpo_clicado, mouse_pos)
                            mouse_joint.max_force = 250000
                            espaco.add(mouse_joint)

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    if mouse_joint:
                        espaco.remove(mouse_joint)
                        mouse_joint = None
                    ponto_arrastando = None

            # --- TECLAS DE ATALHO ---
            elif evento.type == pygame.KEYDOWN:
                info_hover = espaco.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())

                # TECLA 'R': Criar Corda
                if evento.key == pygame.K_r:
                    if info_hover: # Pode pregar no chão (estático) ou blocos (dinâmico)
                        corpo_alvo = info_hover.shape.body

                        if corpo_corda_a is None:
                            # Primeiro clique: define o ponto A
                            corpo_corda_a = corpo_alvo
                            # Guarda a posição relativa do clique dentro do bloco
                            ancora_a_local = corpo_alvo.world_to_local(mouse_pos)
                            print("Ponto 1 da corda fixado! Aperte 'R' em outro lugar para amarrar.")
                        else:
                            # Segundo clique: define o ponto B e cria a corda
                            corpo_b = corpo_alvo
                            ancora_b_local = corpo_b.world_to_local(mouse_pos)

                            # Descobrir a posição atual dos dois pontos no mundo para calcular o tamanho
                            pos_a_mundo = corpo_corda_a.local_to_world(ancora_a_local)
                            pos_b_mundo = corpo_b.local_to_world(ancora_b_local)

                            # Teorema de Pitágoras para saber o comprimento inicial da corda
                            dx = pos_b_mundo[0] - pos_a_mundo[0]
                            dy = pos_b_mundo[1] - pos_a_mundo[1]
                            distancia = math.sqrt(dx**2 + dy**2)

                            # Criar a SlideJoint (min: 0, max: distancia)
                            corda = pymunk.SlideJoint(corpo_corda_a, corpo_b, ancora_a_local, ancora_b_local, 0, distancia)
                            espaco.add(corda)
                            print("Corda criada!")

                            # Resetar para a próxima corda
                            corpo_corda_a = None
                            ancora_a_local = None

                elif info_hover and info_hover.shape.body.body_type == pymunk.Body.DYNAMIC:
                    # TECLA 'P': Pregar (Pin estático)
                    if evento.key == pygame.K_p:
                        pino = pymunk.PivotJoint(info_hover.shape.body, espaco.static_body, mouse_pos)
                        espaco.add(pino)
                        print("Bloco pregado!")

                    # TECLA 'C': Alternar Colisão
                    elif evento.key == pygame.K_c:
                        info_hover.shape.sensor = not info_hover.shape.sensor

        # --- Lógica de Movimentação ---
        # Se estiver arrastando um ponto azul, a posição dele é setada manualmente
        if ponto_arrastando:
            ponto_arrastando.position = mouse_pos

        # Se estiver arrastando um bloco, a junta cuida da física
        if mouse_joint:
            mouse_body.position = mouse_pos

        # Atualiza a posição do mouse
        if mouse_joint:
            mouse_body.position = mouse_pos

        # --- Passo da Física ---
        espaco.step(1 / 60.0)

        # --- Desenho ---
        espaco.debug_draw(opcoes_desenho)

        # Visual extra para os pontos de controle (Blue Glow)
        for p in pontos_controle:
            pygame.draw.circle(tela, (0, 100, 255), (int(p.position.x), int(p.position.y)), 15, 2)

        # Desenhar uma linha vermelha de "pré-visualização" se o jogador estiver criando uma corda
        if corpo_corda_a is not None:
            # Pega onde o ponto A está agora (caso o bloco tenha caído enquanto o jogador move o mouse)
            pos_atual_a = corpo_corda_a.local_to_world(ancora_a_local)
            pygame.draw.line(tela, (255, 0, 0), pos_atual_a, mouse_pos, 2)

        # Instruções
        fonte = pygame.font.SysFont(None, 24)
        tela.blit(fonte.render("Clique Esquerdo: Pegar bloco", True, (0,0,0)), (10, 10))
        #tela.blit(fonte.render("Mouse + 'P': Colocar um Prego fixo", True, (0,0,0)), (10, 30))
        #tela.blit(fonte.render("Mouse + 'C': Ligar/Desligar colisão", True, (0,0,0)), (10, 50))
        #tela.blit(fonte.render("Mouse + 'R': Ponto 1 da Corda -> Mouse + 'R': Ponto 2", True, (0,0,200)), (10, 70))

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
jogo()