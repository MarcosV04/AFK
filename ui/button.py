import pygame

class Button:
    
    def __init__(self, text, x, y, width, height, font_size=48):
        self.text = text
        self.base_width = width
        self.base_height = height
        
        # O self.rect define a posição fixa e a área principal de colisão
        self.rect = pygame.Rect(x, y, width, height)
        
        # --- CARREGAMENTO DAS SPRITES ---
        try:
            # Carrega as imagens com suporte a transparência (.png)
            self.img_normal = pygame.image.load("assets/images/menu/Btn_normal.png").convert_alpha()
            self.img_hover = pygame.image.load("assets/images/menu/Btn_hover.png").convert_alpha()
            self.img_pressed = pygame.image.load("assets/images/menu/Btn_pressed.png").convert_alpha()
            
            # Redimensiona as sprites originais para o tamanho base do botão
            self.img_normal = pygame.transform.smoothscale(self.img_normal, (width, height))
            self.img_hover = pygame.transform.smoothscale(self.img_hover, (width, height))
            self.img_pressed = pygame.transform.smoothscale(self.img_pressed, (width, height))
            
        except pygame.error as e:
            
            print(f"Aviso: Não foi possível carregar as sprites do botão ({e}). Usando fallback visual.")
            # Caso as imagens ainda não existam na pasta, cria superfícies de rascunho para não quebrar o jogo
            self.img_normal = pygame.Surface((width, height), pygame.SRCALPHA)
            self.img_hover = self.img_normal.copy()
            self.img_pressed = self.img_normal.copy()
            self.img_pressed.fill((15, 12, 8), special_flags = pygame.BLEND_RGBA_MULT)
            
            pygame.draw.rect(self.img_normal, (28, 22, 14), (0, 0, width, height), border_radius=12)
            pygame.draw.rect(self.img_normal, (212, 175, 55), (0, 0, width, height), width=3, border_radius=12)
            pygame.draw.rect(self.img_hover, (255, 225, 130), (0, 0, width, height), width=3, border_radius=12)
            
        # Cor do Texto (Bege do exemplo)
        self.text_color = (230, 210, 160)
        
        # Fonte (Se a fonte 'Cinzel' não estiver no sistema, o Pygame usa a padrão)
        self.font = pygame.font.SysFont("Cinzel", font_size, bold=True)
        
        # Estados e Variáveis de Animação
        self.is_hovered = False
        self.pressed = False
        self.scale = 1.0
        self.target_scale = 1.0

    def update(self):
        # Verifica se o mouse está sobre a área do botão
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Controla o tamanho alvo para o efeito elástico de zoom (hover)
        if self.is_hovered:
            self.target_scale = 1.03          # Aumenta 6% quando o mouse passa
        else:
            self.target_scale = 1.0           # Tamanho normal
        
        # Interpolação matemática suave (sua lógica original mantida)
        self.scale += (self.target_scale - self.scale) * 0.12

    def draw(self, screen):
        # Garante que a lógica rode antes do desenho
        self.update()
        
        # 1. Escolhe a sprite correta de acordo com o estado do botão
        if self.pressed:
            current_img = self.img_pressed
        elif self.is_hovered:
            current_img = self.img_hover
        else:
            current_img = self.img_normal
            
        # 2. Calcula o tamanho animado mantendo o centro no mesmo lugar
        new_width = int(self.base_width * self.scale)
        new_height = int(self.base_height * self.scale)
        animated_rect = pygame.Rect(self.rect.centerx - new_width // 2, self.rect.centery - new_height // 2, new_width, new_height)
        
        # 3. Redimensiona dinamicamente a sprite escolhida para encaixar no tamanho da animação
        scaled_img = pygame.transform.smoothscale(current_img, (new_width, new_height))
        
        # 4. Desenha a imagem na tela
        screen.blit(scaled_img, animated_rect)
        
        # 5. Renderiza o texto centralizado por cima da imagem
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=animated_rect.center)
        
        # Efeito de clique: desloca o texto levemente para baixo para dar sensação de profundidade
        offset_y = 0

        if self.pressed:
            offset_y = 2

        animated_rect.y += offset_y
        text_rect.y += offset_y
            
        screen.blit(text_surf, text_rect)
        
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
            
                if self.rect.collidepoint(event.pos):
                    self.pressed = True
                    return True
    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.pressed = False
    
        return False
