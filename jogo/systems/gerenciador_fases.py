import pygame
import pymunk
import random

class GerenciadorFases:
    # Adicionamos "sons" aqui no final
    def __init__(self, espaco, largura, altura, mapa_atual, sons):
        self.espaco = espaco
        self.largura = largura
        self.altura = altura
        self.mapa_atual = mapa_atual 
        self.sons = sons 

        self.tempo_inicio = pygame.time.get_ticks()
        self.ultimo_spawn = self.tempo_inicio
        
        self.intervalo_spawn = 3000 
        self.dificuldade = 1.0
        
        self.inicio_voo = 0
        self.voando = False
        self.punicao_ativa = False
        
        # NOVO: Lista para rastrear o tempo de vida e a posição de cada objeto
        self.obstaculos_ativos = []

    def update(self, tempo_atual, boneco):
        # 1. Progressão
        tempo_decorrido = tempo_atual - self.tempo_inicio
        self.dificuldade = 1.0 + (tempo_decorrido / 20000)
        intervalo_atual = max(600, int(self.intervalo_spawn / self.dificuldade))
        
        # 2. Spawner
        if tempo_atual - self.ultimo_spawn > intervalo_atual:
            self.gerar_obstaculo(tempo_atual)
            self.ultimo_spawn = tempo_atual
            
        # 3. NOVO: Gerenciamento de Vida (Limpeza e Movimento Constante)
        self.limpar_e_mover_obstaculos(tempo_atual)

        # 4. Fiscal de Voo
        return self.verificar_anti_voo(tempo_atual, boneco)

    def limpar_e_mover_obstaculos(self, tempo_atual):
        # Iteramos de trás pra frente (usando [:]) para poder deletar itens da lista com segurança
        for obs in self.obstaculos_ativos[:]:
            corpo = obs["corpo"]
            forma = obs["forma"]
            tipo = obs["tipo"]
            criacao = obs["criacao"]
            remover = False

            # Se a flecha já sumiu porque bateu no boneco ou no chão (lógica do game.py)
            if forma not in self.espaco.shapes:
                self.obstaculos_ativos.remove(obs)
                continue

            # --- LÓGICAS ESPECÍFICAS DE CADA OBSTÁCULO ---
            if tipo == "espinho":
                # Some após 5s OU se tocar no chão (Centro Y fica perto de altura - 70)
                if tempo_atual - criacao > 5000 or corpo.position.y > self.altura - 75:
                    remover = True
                    
            elif tipo == "onda":
                # Força Constante: Sobrescreve a velocidade X para ela não parar nunca
                corpo.velocity = (350, corpo.velocity.y)
                # Some quando sair da tela pela direita
                if corpo.position.x > self.largura + 100:
                    remover = True
                    
            elif tipo == "canhao":
                # Some após 6 segundos
                if tempo_atual - criacao > 6000:
                    remover = True
                    
            elif tipo == "flecha":
                # Some se voar para fora da tela (caso não bata em nada)
                if corpo.position.x > self.largura + 100 or corpo.position.x < -100:
                    remover = True

            # DESTRUIÇÃO FÍSICA
            if remover:
                self.espaco.remove(corpo, forma)
                self.obstaculos_ativos.remove(obs)

    def gerar_obstaculo(self, tempo_atual):
        opcoes = []
        if self.mapa_atual == "teatro":
            opcoes = ["flecha", "espinho"]
        elif self.mapa_atual == "praia":
            opcoes = ["onda", "canhao"]
        else: 
            opcoes = ["flecha", "espinho", "onda", "canhao"]
            
        escolha = random.choice(opcoes)
        
        if escolha == "flecha": self.atirar_flecha(tempo_atual)
        elif escolha == "espinho": self.cair_espinho(tempo_atual)
        elif escolha == "onda": self.gerar_onda(tempo_atual)
        elif escolha == "canhao": self.atirar_canhao(tempo_atual)

    # Note que agora salvamos todos eles na lista obstaculos_ativos
    def atirar_flecha(self, tempo_atual):
        corpo = pymunk.Body(5, pymunk.moment_for_box(5, (60, 10)))
        corpo.position = (10, random.randint(100, self.altura - 150))
        forma = pymunk.Poly.create_box(corpo, (60, 10))
        forma.collision_type = 2
        forma.color = (255, 0, 0, 255)
        self.espaco.add(corpo, forma)
        corpo.apply_impulse_at_local_point((15000, -500))
        self.sons["disparo_flecha"].play() 
        self.obstaculos_ativos.append({"corpo": corpo, "forma": forma, "tipo": "flecha", "criacao": tempo_atual})

    def atirar_canhao(self, tempo_atual):
        corpo = pymunk.Body(50, pymunk.moment_for_circle(50, 0, 30))
        corpo.position = (10, self.altura // 2 - 100)
        forma = pymunk.Circle(corpo, 30)
        forma.collision_type = 3
        forma.elasticity = 0.8
        forma.color = (50, 50, 50, 255)
        self.espaco.add(corpo, forma)
        corpo.apply_impulse_at_local_point((80000, -15000))
        self.sons["disparo_canhao"].play()
        self.obstaculos_ativos.append({"corpo": corpo, "forma": forma, "tipo": "canhao", "criacao": tempo_atual})

    def cair_espinho(self, tempo_atual):
        corpo = pymunk.Body(20, pymunk.moment_for_box(20, (40, 40)))
        corpo.position = (random.randint(100, self.largura - 100), -50)
        forma = pymunk.Poly.create_box(corpo, (40, 40))
        forma.collision_type = 3
        forma.color = (150, 0, 150, 255)
        self.espaco.add(corpo, forma)
        self.sons["disparo_espinho"].play()
        self.obstaculos_ativos.append({"corpo": corpo, "forma": forma, "tipo": "espinho", "criacao": tempo_atual})

    def gerar_onda(self, tempo_atual):
        corpo = pymunk.Body(100, pymunk.moment_for_box(100, (160, 100)))
        corpo.position = (10, self.altura - 75)
        forma = pymunk.Poly.create_box(corpo, (80, 50))
        forma.collision_type = 3
        forma.color = (0, 100, 255, 255)
        forma.friction = 0.0 
        self.espaco.add(corpo, forma)
        self.sons["disparo_onda"].play()
        self.obstaculos_ativos.append({"corpo": corpo, "forma": forma, "tipo": "onda", "criacao": tempo_atual})

    def verificar_anti_voo(self, tempo_atual, boneco):
        torco = boneco["torco"]
        if torco.body.position.y < 250:
            if not self.voando:
                self.voando = True
                self.inicio_voo = tempo_atual
            elif tempo_atual - self.inicio_voo > 3000:
                self.punicao_ativa = True
                torco.body.apply_force_at_local_point((0, 80000), (0,0))
        else:
            self.voando = False
            if torco.body.position.y > self.altura - 150:
                self.punicao_ativa = False
        return self.punicao_ativa