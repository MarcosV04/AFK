import pygame
import pymunk
import pymunk.pygame_util
import math
import os

from fisica.mundo import criar_chao, criar_bloco, criar_corda
from entidades.boneco import criar_boneco
from jogo.states.menu_jogo import desenhar_menu
from camera.controle import atualizar_camera
from jogo.systems.skins import carregar_skin_pasta, carregar_thumbs
from jogo.systems.textura import load_sprites
from jogo.systems.cenario import load_cenario_texturas


class game:

    def __init__(self, largura, altura, fila, config, gestos, skin):

        self.LARGURA = largura
        self.ALTURA = altura
        self.fila = fila
        self.config = config
        self.gestos = gestos
        self.skin = skin
        self.fonte = pygame.font.SysFont(None, 24)

        # FÍSICA
        self.espaco = pymunk.Space()
        self.espaco.gravity = (0, 981)

        # ESTADOS
        self.mostrar_debug = False
        self.menu_aberto = False
        self.janela_skins_aberta = False
        self.conexao_garra = None
        self.ponto_arrastando = None
        self.mouse_joint = None
        self.modo_edicao = False
        self.sinal_ativo = False
        self.sair_partida = False
        
        # SPRITES
        self.sprites_boneco = carregar_skin_pasta(self.skin)
        self.texturas = load_sprites("assets/texturas")
        self.texturas_cenario = load_cenario_texturas("assets/mapas")
        self.skins_disponiveis = (
            os.listdir("assets/skins")
            if os.path.exists("assets/skins")
            else []
        )

        self.thumbs_skins = carregar_thumbs(self.skins_disponiveis)

        # PONTOS CONTROLE
        self.pontos_controle = []
        for i in range(5):
            corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            corpo.position = ((self.LARGURA // 2) - 200 + (i * 100), 150)
            forma = pymunk.Circle(corpo, 15)
            forma.sensor = True
            forma.collision_type = 1

            self.espaco.add(corpo, forma)
            self.pontos_controle.append(corpo)

        # CENÁRIO
        criar_chao(self.espaco, self.LARGURA, self.ALTURA)
        self.objetos = {}
        self.objetos["espada"] = (criar_bloco(self.espaco, self.LARGURA // 2 + 200, 100, altura=100, largura=20, massa=50),(altura, largura))
        self.objetos["box"] = (criar_bloco(self.espaco, self.LARGURA // 2 - 200, 100, altura=100, largura=100, massa=100),(altura, largura))
        self.meu_boneco = criar_boneco(self.espaco, self.pontos_controle, self.LARGURA)
        
        # MOUSE
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)

        # MENU e BTS
        self.rect_abrir_menu = pygame.Rect(self.LARGURA - 150, 10, 140, 40)

        # MENU e BTS
        self.rect_abrir_menu = pygame.Rect(self.LARGURA - 150, 10, 140, 40)
        self.rect_continuar = pygame.Rect(self.LARGURA - 240, 110, 200, 40)
        self.rect_sair = pygame.Rect(self.LARGURA - 240, 170, 200, 40)

        # Teclado
        self.velocidade_teclado = 10

    def handle_events(self, event):

        mouse_pos = pygame.mouse.get_pos()

        # TECLADO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.modo_edicao = not self.modo_edicao
                self.mostrar_debug = not self.mostrar_debug
                print("Modo edição:", self.modo_edicao)
            if event.key == pygame.K_j:
                self.sinal_ativo = not self.sinal_ativo
                print("Sinal ativo:", self.sinal_ativo)

        # MOUSE APERTADo
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                # MENU
                if self.rect_abrir_menu.collidepoint(mouse_pos):
                    print("Funciona o menu")
                    self.menu_aberto = not self.menu_aberto
                    
                # BOTÕES DO MENU
                elif self.menu_aberto:
                
                    if self.rect_continuar.collidepoint(mouse_pos):
                        self.menu_aberto = False

                    elif self.rect_sair.collidepoint(mouse_pos):
                        self.sair_partida = True   
                else:
                    info = self.espaco.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())

                    if info and info.shape:
                        corpo = info.shape.body

                        # PONTOS AZUIS
                        if corpo in self.pontos_controle:
                            self.ponto_arrastando = corpo

                        # OBJETOS DINÂMICOS
                        elif corpo.body_type == pymunk.Body.DYNAMIC:
                            if self.mouse_joint is None:
                                self.mouse_body.position = mouse_pos
                                self.mouse_joint = pymunk.PivotJoint(self.mouse_body, corpo, mouse_pos)
                                self.mouse_joint.max_force = 250000
                                self.espaco.add(self.mouse_joint)

        # SOLTOU MOUSE
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.ponto_arrastando = None
                if self.mouse_joint:
                    self.espaco.remove(self.mouse_joint)
                    self.mouse_joint = None

    def update(self):

        mouse_pos = pygame.mouse.get_pos()
        atualizar_camera(self.fila, self.pontos_controle, self.modo_edicao)

        # GESTOS
        acao = "Parado"

        if self.gestos is not None and not self.gestos.empty():
            try:
                acao = self.gestos.get_nowait()

            except Exception as erro:

                print("ERRO:", erro)

        sinal_ativo = (acao == "Agachar")

        # MOVIMENTO
        if self.ponto_arrastando is not None:
            self.ponto_arrastando.position = mouse_pos

        if self.mouse_joint:
            self.mouse_body.position = mouse_pos

        # GARRA
        braco_dir = self.meu_boneco["antdir"]
        pos_mao = braco_dir.body.local_to_world((0, 25))
        raio = 40

        if self.sinal_ativo:
            if self.conexao_garra is None:
                info = self.espaco.point_query_nearest(pos_mao, raio, pymunk.ShapeFilter())

                if (info and info.shape.body.body_type == pymunk.Body.DYNAMIC and info.shape.body != braco_dir.body):
                    self.conexao_garra = pymunk.PivotJoint(braco_dir.body, info.shape.body, pos_mao)
                    self.conexao_garra.max_force = 500000
                    self.espaco.add(self.conexao_garra)
        else:
            if self.conexao_garra:
                self.espaco.remove(self.conexao_garra)
                self.conexao_garra = None
        self.espaco.step(1 / 60)

    def draw(self, screen):

        screen.fill((240, 240, 240))
        self.fundo=self.texturas_cenario["teatro"]
        self.fundo=pygame.transform.scale(self.fundo, (self.LARGURA, self.ALTURA))
        screen.blit(self.fundo, (0, 0))

        # CHÃO
        pygame.draw.line(screen, (50, 50, 50), (0, self.ALTURA - 50), (self.LARGURA, self.ALTURA - 50), 5)

        # CORDAS
        for conexao in self.espaco.constraints:
            if conexao == self.conexao_garra:
                continue

            pos_a = conexao.a.local_to_world(conexao.anchor_a)
            pos_b = conexao.b.local_to_world(conexao.anchor_b)
            pygame.draw.line(screen, (70, 40, 20), pos_a, pos_b, 2)

        # DEBUG/SKIN
        if self.mostrar_debug:
            opcoes = pymunk.pygame_util.DrawOptions(screen)
            self.espaco.debug_draw(opcoes)
        else:
            if self.sprites_boneco:
                for nome, img in self.sprites_boneco.items():
                    forma = self.meu_boneco[nome]
                    corpo = forma.body
                    img_rot = pygame.transform.rotate(img, -math.degrees(corpo.angle))
                    rect = img_rot.get_rect(center=corpo.position)
                    screen.blit(img_rot, rect)
            if self.texturas:
                for nome, img in self.texturas.items():
                    forma = self.objetos[nome]
                    corpo = forma[0].body
                    img_esc=pygame.transform.scale(img, (forma[1][0]/10, forma[1][1]/10))
                    img_rot = pygame.transform.rotate(img_esc, -math.degrees(corpo.angle))
                    rect = img_rot.get_rect(center=corpo.position)
                    screen.blit(img_rot, rect)

        # PONTOS CONTROLE
        for p in self.pontos_controle:
            pygame.draw.circle(screen, (0, 100, 255), (int(p.position.x), int(p.position.y)), 15, 2)

        # GARRA VISUAL
        if self.conexao_garra or self.sinal_ativo:
            braco_dir = self.meu_boneco["antdir"]
            pos_mao = braco_dir.body.local_to_world((0, 25))
            pygame.draw.circle(screen, (0, 255, 0), (int(pos_mao.x), int(pos_mao.y)), 40, 2)

        # MENU
        desenhar_menu(screen, self.fonte, self.rect_abrir_menu, self.menu_aberto, self.LARGURA)