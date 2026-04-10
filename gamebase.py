import pygame
import pymunk
import pymunk.pygame_util
import math

# --- Configurações Iniciais ---
pygame.init()
LARGURA, ALTURA = 1280, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulador de Física com Cordas")
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
def criar_corda(espaco, corpo_a, corpo_b, ancora_a, ancora_b, comprimento):
    corda = pymunk.SlideJoint(corpo_a, corpo_b, ancora_a, ancora_b, 0, comprimento)
    espaco.add(corda)
    return corda
# --- NOVO: Criando os 5 Pontos de Controle (Cinemáticos) ---
pontos_controle = []
for i in range(5):
    # Body_type KINEMATIC faz com que ignore gravidade e forças
    corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    corpo.position = (300 + (i * 100), 50)
    forma = pymunk.Circle(corpo, 15)
    forma.color = (0, 100, 255, 255) # Azul para identificar
    forma.sensor = True # Para não "atropelar" os blocos fisicamente se você não quiser
    espaco.add(corpo, forma)
    pontos_controle.append(corpo)

# Criar o cenário
criar_chao(espaco)
bloco1 = criar_bloco(espaco, 500, 210, 75, 125)
bloco2 = criar_bloco(espaco, 500, 90, 80, 80)
bloco3 = criar_bloco(espaco, 450, 200, 25, 50) 
bloco4 = criar_bloco(espaco, 450, 275, 25, 50)
bloco5 = criar_bloco(espaco, 550, 200, 25, 50) 
bloco6 = criar_bloco(espaco, 550, 275, 25, 50)
bloco7 = criar_bloco(espaco, 475, 325, 25, 50) 
bloco8 = criar_bloco(espaco, 475, 400, 25, 50)
bloco9 = criar_bloco(espaco, 525, 325, 25, 50) 
bloco10 = criar_bloco(espaco, 525, 400, 25, 50)
criar_corda(espaco, bloco1.body, bloco2.body, (0, -62.5), (0, 40), 25)
criar_corda(espaco, bloco1.body, bloco3.body, (-37.5, -50), (0, -25), (math.hypot(15, 15)))
criar_corda(espaco, bloco3.body, bloco4.body, (0, 25), (0, -25), 25)
criar_corda(espaco, bloco1.body, bloco5.body, (37.5, -50), (0, -25), (math.hypot(15, 15)))
criar_corda(espaco, bloco5.body, bloco6.body, (0, 25), (0, -25), 25)
criar_corda(espaco, bloco1.body, bloco7.body, (-25, 65), (0, -25), 25)
criar_corda(espaco, bloco7.body, bloco8.body, (0, 25), (0, -25), 25)
criar_corda(espaco, bloco1.body, bloco9.body, (25, 65), (0, -25), 25)
criar_corda(espaco, bloco9.body, bloco10.body, (0, 25), (0, -25), 25)
criar_corda(espaco, pontos_controle[2], bloco2.body, (0, 0), (0, -40), 100)
criar_corda(espaco, pontos_controle[0], bloco4.body, (0, 0), (0, 25), 250)
criar_corda(espaco, pontos_controle[4], bloco6.body, (0, 0), (0, 25), 250)
criar_corda(espaco, pontos_controle[1], bloco8.body, (0, 0), (0, 25), 475)
criar_corda(espaco, pontos_controle[3], bloco10.body, (0, 0), (0, 25), 475)

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
    tela.blit(fonte.render("Mouse + 'P': Colocar um Prego fixo", True, (0,0,0)), (10, 30))
    tela.blit(fonte.render("Mouse + 'C': Ligar/Desligar colisão", True, (0,0,0)), (10, 50))
    tela.blit(fonte.render("Mouse + 'R': Ponto 1 da Corda -> Mouse + 'R': Ponto 2", True, (0,0,200)), (10, 70))

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()