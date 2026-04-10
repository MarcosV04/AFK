
def jogo():
    import pygame
    import pymunk
    import pymunk.pygame_util
    import math   
    import cv2
    import mediapipe as mp
    import math
    
    # --- Configurações Iniciais ---
    pygame.init()
    LARGURA, ALTURA = 1280, 720
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("🎭 AFK - Away From the Keyboard")
    relogio = pygame.time.Clock()

    # --- Configuração da Física (Pymunk) ---
    espaco = pymunk.Space()
    espaco.gravity = (0, 1800) 
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
        criar_corda(espaco, pontos_controle[0], antesq.body, (0, 0), (0, 25), 100)
        criar_corda(espaco, pontos_controle[4], antdir.body, (0, 0), (0, 25), 100)
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
    
    #Inicio do detector de mãos
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7)

    cap = cv2.VideoCapture(0)

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
        
        success, img = cap.read()
        if not success:
            print("Erro ao acessar a câmera")
            break

        img = cv2.flip(img, 1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        h, w, _ = img.shape

        # Variável global
        movimento = "Parado"
        acao = "Parado"

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                label = results.multi_handedness[idx].classification[0].label

                cor = (0, 255, 0) if label == "Right" else (0, 0, 255)

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                pontos = []

                for lm in hand_landmarks.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    pontos.append((x, y))
                    cv2.circle(img, (x, y), 5, cor, -1)

                if len(pontos) != 21:
                    continue

                # Mao direita para movimentoção
                if label == "Right":
                    cx = pontos[0][0]
                    cy = pontos[0][1]

                    centro_x = w // 2
                    centro_y = h // 2

                    zona = 100  # Regulando ainda

                    if abs(cx - centro_x) < zona and abs(cy - centro_y) < zona:
                        movimento = "Parado"

                    elif cx < centro_x - zona:
                        movimento = "Esquerda"

                    elif cx > centro_x + zona:
                        movimento = "Direita"

                    elif cy < centro_y - zona:
                        movimento = "Frente"

                    elif cy > centro_y + zona:
                        movimento = "Tras"

                # Mao esquerda para acão
                if label == "Left":

                    dedos_levantados = []

                    polegar = pontos[4]
                    pulso = pontos[0]
                    base = pontos[5]

                    dist_polegar = math.hypot(polegar[0] - pulso[0], polegar[1] - pulso[1])
                    dist_base = math.hypot(base[0] - pulso[0], base[1] - pulso[1])

                    if dist_polegar > dist_base * 1.2:
                        dedos_levantados.append("Polegar")

                    if pontos[8][1] < pontos[6][1]:
                        dedos_levantados.append("Indicador")

                    if pontos[12][1] < pontos[10][1]:
                        dedos_levantados.append("Medio")

                    if pontos[16][1] < pontos[14][1]:
                        dedos_levantados.append("Anelar")

                    if pontos[20][1] < pontos[18][1]:
                        dedos_levantados.append("Mindinho")

                    if len(dedos_levantados) == 0:
                        acao = "Agachar"

                    elif "Indicador" in dedos_levantados:
                        acao = "Pular"

                    elif "Polegar" in dedos_levantados:
                        acao = "Especial"

                    else:
                        acao = "Parado"
                        
            pontos_controle[0].position = ((pontos[4][0])*2+LARGURA//4, pontos[4][1]) # Esquerda
            pontos_controle[1].position = ((pontos[8][0])*2+LARGURA//4, pontos[8][1]) # Frente
            pontos_controle[2].position = ((pontos[12][0])*2+LARGURA//4, pontos[12][1])       # Cima
            pontos_controle[3].position = ((pontos[16][0])*2+LARGURA//4, pontos[16][1]) # Tras
            pontos_controle[4].position = ((pontos[20][0])*2+LARGURA//4, pontos[20][1]) # Direita
        
        # Mostra na câmera o movimento e acão detectados
        cv2.putText(img, f"Movimento: {movimento}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(img, f"Acao: {acao}", (10, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("AFK - Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        pygame.display.flip()
        relogio.tick(1200)
    
    cap.release()
    cv2.destroyAllWindows()

    pygame.quit()
jogo()