import pygame
import pymunk
import pymunk.pygame_util
import math
import os

def jogo(fila,config,gestos):
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

    janela_skins_aberta = False
    global thumbs_skins
    thumbs_skins = {} # Dicionário para guardar as imagens da cabeça
    skins_disponiveis = os.listdir("skins") if os.path.exists("skins") else []
    mostrar_debug = False # Começa no modo visual (skins)

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
        criar_corda(espaco, pontos_controle[0], antesq.body, (0, 0), (0, 25), 150)
        criar_corda(espaco, pontos_controle[4], antdir.body, (0, 0), (0, 25), 150)
        criar_corda(espaco, pontos_controle[1], peresq.body, (0, 0), (0, 25), 400)
        criar_corda(espaco, pontos_controle[3], perdir.body, (0, 0), (0, 25), 400)
        partes = {
            "torco": torco,
            "cabeca": cabeca,
            "antesq": antesq,
            "antdir": antdir,
            "panesq": panesq,
            "pandir": pandir,
            "bresq": bresq,
            "bradir": bradir,
            "cintura": cintura,
            "peresq": peresq,
            "perdir": perdir
        }

        return partes
    # --- Dicionário para armazenar as Sprites ---
    global sprites_boneco
    sprites_boneco = {} # { "cabeca": Surface, "torco": Surface, ... }

    def carregar_skin_pasta(nome_pasta):
        global sprites_boneco
        caminho = f"skins/{nome_pasta}"
        partes = ["cabeca", "torco", "bresq", "antesq", "bradir", "antdir", "peresq", "panesq", "perdir", "pandir"]
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
        for parte in partes:
            arq = f"{caminho}/{parte}.png"
            if os.path.exists(arq):
                img = pygame.image.load(arq).convert_alpha()
                # Precisamos saber o tamanho do bloco para redimensionar a imagem
                # Ex: torco tem 75x90 no seu código
                sprites_boneco[parte] = img
        for parte, dimensoes in tamanhos.items():
                arq = f"{caminho}/{parte}.png"
                if os.path.exists(arq):
                    # 1. Carrega a imagem original
                    img_original = pygame.image.load(arq).convert_alpha()
                    # 2. REDIMENSIONA para o tamanho do bloco físico
                    img_redimensionada = pygame.transform.scale(img_original, dimensoes)
                    # 3. Guarda a imagem pronta no dicionário
                    sprites_boneco[parte] = img_redimensionada
    #criar_boneco()
    meu_boneco = criar_boneco()


    def carregar_thumbnails():
        global thumbs_skins
        for pasta in skins_disponiveis:
            caminho_thumb = f"skins/{pasta}/cabeca.png"
            if os.path.exists(caminho_thumb):
                img = pygame.image.load(caminho_thumb).convert_alpha()
                # Redimensiona para um tamanho de ícone (ex: 60x60)
                thumbs_skins[pasta] = pygame.transform.scale(img, (60, 60))

    carregar_thumbnails()


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

    # --- Estados do Menu ---
    menu_aberto = False
    skin_atual = "padrao"
    skins_disponiveis = os.listdir("skins") if os.path.exists("skins") else []
    indices_skin = 0

    # --- Variáveis da Garra ---
    conexao_garra = None
    sinal_ativo = False
    rodando = True
    while rodando:
        tela.fill((240, 240, 240)) # Fundo cinza claro
        mouse_pos = pygame.mouse.get_pos()
        pos_interacao = mouse_pos # Ponto usado para clicar no menu (dedo indicador ou mouse)
        if gestos is not None and not gestos.empty():
            acao=gestos.get()
        
        rect_menu = pygame.Rect(LARGURA//2 - 150, ALTURA//2 - 150, 300, 400)
        rect_btn_skin = pygame.Rect(LARGURA//2 - 100, ALTURA//2 - 50, 200, 50)
        rect_btn_sair = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 50, 200, 50)
        rect_btn_fechar_menu = pygame.Rect(LARGURA//2 - 100, ALTURA//2 + 150, 200, 50)
        braco_dir = meu_boneco["antdir"]
        pos_mao_boneco = braco_dir.body.local_to_world((0, 25))

        rect_abrir_menu = pygame.Rect(LARGURA - 150, 10, 140, 40)
        
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

                if evento.key == pygame.K_k:
                    # Mover os pontos de controle para formar uma linha horizontal seguindo o mouse
                    pontos_controle[0].position=(mouse_pos[0]-200, mouse_pos[1])
                    pontos_controle[1].position=(mouse_pos[0]-100, mouse_pos[1])
                    pontos_controle[2].position=(mouse_pos[0], mouse_pos[1])
                    pontos_controle[3].position=(mouse_pos[0]+100, mouse_pos[1])
                    pontos_controle[4].position=(mouse_pos[0]+200, mouse_pos[1])
                try:
                    if evento.key == pygame.K_m or acao == "Agachar":
                        sinal_ativo = True # Substitua pela sua lógica de sinal vindo da fila
                except:
                    pass
                try:
                    if evento.key == pygame.K_n or acao != "Agachar":
                        sinal_ativo = False # Substitua pela sua lógica de sinal vindo da fila
                except:
                    pass
                
                if evento.key == pygame.K_h: # Tecla 'H' para 'Hitbox'
                    mostrar_debug = not mostrar_debug
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
        pygame.draw.line(tela, (50, 50, 50), (0, ALTURA - 50), (LARGURA, ALTURA - 50), 5)

        if sprites_boneco:
            for nome, img in sprites_boneco.items():
                forma = meu_boneco[nome]
                corpo = forma.body
                img_rot = pygame.transform.rotate(img, -math.degrees(corpo.angle))
                rect = img_rot.get_rect(center=corpo.position)
                tela.blit(img_rot, rect)
                # 1. DESENHO DAS CORDAS (Manual)
                # Percorre todas as conexões físicas (SlideJoints, PivotJoints, etc.)
                for conexao in espaco.constraints:
                    # Ignora a conexão da "garra" se não quiser que ela apareça como linha
                    if conexao == conexao_garra:
                        continue

                    # Pega as posições reais dos pontos A e B da corda no mundo
                    pos_a = conexao.a.local_to_world(conexao.anchor_a)
                    pos_b = conexao.b.local_to_world(conexao.anchor_b)

                    # Desenha a linha da corda (marrom ou preto)
                    pygame.draw.line(tela, (70, 40, 20), pos_a, pos_b, 2)

                # 2. LOGICA DE VISIBILIDADE (O que o usuário vê)
                if mostrar_debug:
                    # Volta ao "Normal" (mostra as caixas, círculos e eixos)
                    espaco.debug_draw(opcoes_desenho)
                else:
                    # Modo Imersivo (apenas Skins e o Chão)
                    pygame.draw.line(tela, (50, 50, 50), (0, ALTURA - 50), (LARGURA, ALTURA - 50), 5)

                    if sprites_boneco:
                        for nome, img in sprites_boneco.items():
                            forma = meu_boneco[nome]
                            corpo = forma.body
                            img_rot = pygame.transform.rotate(img, -math.degrees(corpo.angle))
                            rect = img_rot.get_rect(center=corpo.position)
                            tela.blit(img_rot, rect)
        else:
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

        if menu_aberto:
            pygame.draw.rect(tela, (200, 200, 200), rect_menu)
            tela.blit(fonte.render("MENU", True, (255, 255, 255)), (rect_menu[0], rect_menu[1]))
            pygame.draw.rect(tela, (100, 100, 100), rect_btn_skin)
            tela.blit(fonte.render("Skins", True, (255, 255, 255)), (rect_btn_skin[0], rect_btn_skin[1]))
            pygame.draw.rect(tela, (100, 100, 100), rect_btn_fechar_menu)
            tela.blit(fonte.render("FECHAR MENU", True, (255, 255, 255)), (rect_btn_fechar_menu[0], rect_btn_fechar_menu[1]))
            pygame.draw.rect(tela, (100, 100, 100), rect_btn_sair)
            tela.blit(fonte.render("SAIR", True, (255, 255, 255)), (rect_btn_sair[0], rect_btn_sair[1]))
            if sinal_ativo:
                if rect_btn_skin.collidepoint(pos_interacao):
                    janela_skins_aberta = True
                if rect_btn_sair.collidepoint(pos_interacao):
                    rodando = False
                if rect_btn_fechar_menu.collidepoint(pos_interacao):
                    menu_aberto = False
        else:
            pygame.draw.rect(tela, (150, 150, 150), rect_abrir_menu)
            tela.blit(fonte.render("ABRIR MENU", True, (255, 255, 255)), (LARGURA - 140, 20))
        
        if fila is not None:
            tela.blit(fonte.render("Controle por Gestos Ativo", True, (0,200,0)), (10, 30))
            if not fila.empty():
                pontos = fila.get()
                if len(pontos) >= 20:
                    pontos_controle[0].position = ((pontos[4][0])*2, pontos[4][1]*2) # Esquerda
                    pontos_controle[1].position = ((pontos[8][0])*2, pontos[8][1]*2) # Frente
                    pontos_controle[2].position = ((pontos[12][0])*2, pontos[12][1]*2) # Cima
                    pontos_controle[3].position = ((pontos[16][0])*2, pontos[16][1]*2) # Tras
                    pontos_controle[4].position = ((pontos[20][0])*2, pontos[20][1]*2) # Direita
            if not config.empty():
                comando = config.get()
                if comando == "Fechar":
                    rodando = False
            config.put("Fechar")

        if not menu_aberto and sinal_ativo:
            if rect_abrir_menu.collidepoint(pos_interacao):
                menu_aberto = True
        try:
            raio_interacao = 40 # Tamanho do círculo de alcance
            if sinal_ativo:
                # Desenha um círculo semi-transparente ou apenas o contorno na ponta do braço
                pygame.draw.circle(tela, (0, 255, 0), (int(pos_mao_boneco.x), int(pos_mao_boneco.y)), raio_interacao, 2)
                if sinal_ativo and conexao_garra is None:
                    # O sensor agora "escaneia" tudo dentro do raio_interacao ao redor da mão
                    info = espaco.point_query_nearest(pos_mao_boneco, raio_interacao, pymunk.ShapeFilter())

                    if info and info.shape.body.body_type == pymunk.Body.DYNAMIC:
                        corpo_objeto = info.shape.body

                        # Criamos o PivotJoint exatamente na posição da mão do boneco
                        # Isso faz o objeto "grudar" na palma da mão, não importa onde foi tocado
                        conexao_garra = pymunk.PivotJoint(braco_dir.body, corpo_objeto, pos_mao_boneco)
                        conexao_garra.max_force = 500000 # Força para conseguir carregar objetos pesados
                        espaco.add(conexao_garra)
            elif not sinal_ativo and conexao_garra is not None:
                # Quando o sinal para, a conexão é removida do espaço físico
                espaco.remove(conexao_garra)
                conexao_garra = None
        except:
            pass
        try:
            if janela_skins_aberta:
                fundo_skins = pygame.Rect(LARGURA//2 - 250, ALTURA//2 - 200, 500, 400)
                pygame.draw.rect(tela, (230, 230, 230), fundo_skins)
                
                # --- BOTÃO ESPECIAL: DEBUG ---
                # Colocamos ele fixo na primeira posição
                rect_debug = pygame.Rect(fundo_skins.x + 30, fundo_skins.y + 50, 80, 80)
                cor_debug = (0, 255, 0) if mostrar_debug else (150, 150, 150)
                pygame.draw.rect(tela, cor_debug, rect_debug)
                
                # Texto ou ícone simples para o Debug
                tela.blit(fonte.render("DEBUG", True, (0, 0, 0)), (rect_debug.x + 10, rect_debug.y + 30))
                
                if sinal_ativo and rect_debug.collidepoint(pos_interacao):
                    mostrar_debug = not mostrar_debug # Inverte o estado
                    # Opcional: limpa as skins para ver só o esqueleto
                    if mostrar_debug: sprites_boneco = {} 
                    # Pequeno delay para não clicar e desclicar instantaneamente
                    pygame.time.delay(200) 
            
                # --- RESTANTE DAS SKINS (Deslocadas para frente) ---
                for i, nome_skin in enumerate(skins_disponiveis):
                    # Somamos +1 no índice para não ocupar o lugar do botão Debug
                    indice_ajustado = i + 1 
                    coluna = indice_ajustado % 4
                    linha = indice_ajustado // 4
                    x = fundo_skins.x + 30 + (coluna * 110)
                    y = fundo_skins.y + 50 + (linha * 110)
                    
                    rect_thumb = pygame.Rect(x, y, 80, 80)
                    pygame.draw.rect(tela, (200, 200, 200), rect_thumb)
                    
                    if nome_skin in thumbs_skins:
                        tela.blit(thumbs_skins[nome_skin], (x + 10, y + 10))
                    
                    if sinal_ativo and rect_thumb.collidepoint(pos_interacao):
                        carregar_skin_pasta(nome_skin)
                        mostrar_debug = False # Desativa debug ao colocar skin
                        janela_skins_aberta = False
                btn_fechar = pygame.Rect(fundo_skins.right - 30, fundo_skins.top + 5, 25, 25)
                pygame.draw.rect(tela, (255, 0, 0), btn_fechar)
                if sinal_ativo and btn_fechar.collidepoint(pos_interacao):
                    janela_skins_aberta = False
        except:
            pass
        pygame.display.flip()
        relogio.tick(60)
    pygame.quit()
