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

# Criar o cenário
criar_chao(espaco)
bloco1 = criar_bloco(espaco, 300, 100, 100, 50)
bloco2 = criar_bloco(espaco, 500, 100, 60, 60)
bloco3 = criar_bloco(espaco, 400, 300, 80, 20) # Bloco extra para brincar
bloco4 = criar_bloco(espaco, 400, 350, 80, 20)
bloco5 = criar_bloco(espaco, 400, 400, 80, 20) # Bloco extra para brincar
bloco6 = criar_bloco(espaco, 400, 450, 80, 20)
# Variáveis para interação com o mouse
mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
mouse_joint = None

# Variáveis para criação da corda
corpo_corda_a = None
ancora_a_local = None

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
                info_clique = espaco.point_query_nearest(mouse_pos, 0, pymunk.ShapeFilter())
                if info_clique and info_clique.shape.body.body_type == pymunk.Body.DYNAMIC:
                    mouse_body.position = mouse_pos
                    mouse_joint = pymunk.PivotJoint(mouse_body, info_clique.shape.body, mouse_pos)
                    mouse_joint.max_force = 50000
                    mouse_joint.error_bias = (1.0 - 0.15) ** 60
                    espaco.add(mouse_joint)

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and mouse_joint:
                espaco.remove(mouse_joint)
                mouse_joint = None

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

    # Atualiza a posição do mouse
    if mouse_joint:
        mouse_body.position = mouse_pos

    # --- Passo da Física ---
    espaco.step(1 / 60.0)
    
    # --- Desenho ---
    espaco.debug_draw(opcoes_desenho)

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