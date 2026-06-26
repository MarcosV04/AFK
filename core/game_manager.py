import pygame

from multiprocessing import Process, Queue
from jogo.states.tela_main.menu_inicial import menu
from jogo.states.tela_pre_game.pre_game import PreGame
from jogo.states.gameplay.game import game
from jogo.systems.skins import load_skin
from camera.hand_tracking import run_hand_tracking
from jogo.states.tela_pre_game.tela_skins import TelaSkins
from jogo.states.tela_pre_game.tela_config import TelaConfig

class GameManager:

    def __init__(self):

        pygame.init()

        # TELA
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("AFK")
        
        # FILAS
        self.fila = Queue(maxsize=1)
        self.gestos = Queue(maxsize=1)
        self.config = Queue()
        
        # PROCESSO CAMERA
        self.camera_process = None

        # STATES
        self.tela_main = menu(self.WIDTH, self.HEIGHT)
        self.pre_game = PreGame(self.WIDTH, self.HEIGHT)
        self.tela_skins = TelaSkins(self.WIDTH, self.HEIGHT)
        self.tela_config = TelaConfig(self.WIDTH, self.HEIGHT)
        self.gameplay = None

        # STATE ATUAL
        self.current_state = "menu"
        self.running = True
        self.skin_selecionada = "teste"

    def iniciar_camera(self):

        if self.camera_process is None:
            self.camera_process = Process(target=run_hand_tracking, args=(self.fila, self.config, self.gestos))
            self.camera_process.start()
    
    def parar_camera(self):

        if self.camera_process is not None:

            self.config.put("Fechar")

            self.camera_process.join(timeout=3)

            if self.camera_process.is_alive():
                self.camera_process.terminate()
                self.camera_process.join()
            self.camera_process = None
        return

    def run(self):
        pygame.mixer.init()

        # Carregar e tocar música (loop infinito com -1)
        pygame.mixer.music.load('assets/sons/musica/teatro.mp3')
        pygame.mixer.music.set_volume(0.5) # Volume entre 0.0 e 1.0
        pygame.mixer.music.play(-1)
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()
        
        if self.camera_process is not None:

            # avisa a camera para fechar
            self.config.put("Fechar")
        
            # espera ela encerrar corretamente
            self.camera_process.join(timeout = 3)
        
            # segurança extra
            if self.camera_process.is_alive():
                self.camera_process.terminate()
                self.camera_process.join()

            self.camera_process = None
            
        pygame.quit()

    def events(self):

        for event in pygame.event.get():

            # FECHAR JOGO
            if event.type == pygame.QUIT:
                self.running = False

            # ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            # MENU
            if self.current_state == "menu":

                if self.tela_main.handle_events(event):
                    self.current_state = "pre_game"

            # PRE GAME
            elif self.current_state == "pre_game":

                # VOLTAR
                if self.pre_game.back_button.handle_event(event):
                    self.current_state = "menu"

                # SKINS
                if self.pre_game.skin_button.handle_event(event):
                    self.current_state = "skins"

                # CONFIG
                if self.pre_game.config_button.handle_event(event):
                    self.current_state = "config"

                # START
                if self.pre_game.start_button.handle_event(event):
                    
                    try:

                        if self.tela_config.modo_jogo == "AFK":
                            self.iniciar_camera()

                        skin_escolhida = self.pre_game.skins[self.tela_skins.val]
                        self.gameplay = game(self.WIDTH, self.HEIGHT, self.fila, self.config, self.gestos, skin_escolhida)
                        self.current_state = "gameplay"
                        
                    except Exception as erro:
                        print("Erro ao inicializar o jogo:", erro)

            # SKINS
            elif self.current_state == "skins":

                if self.tela_skins.back_button.handle_event(event):
                    self.current_state = "pre_game"

            # CONFIG
            elif self.current_state == "config":
            
                if self.tela_config.back_button.handle_event(event):
                    self.current_state = "pre_game"

                if self.tela_config.modo_button.handle_event(event):
                
                    if self.tela_config.modo_jogo == "AFK":
                        self.tela_config.modo_jogo = "TECLADO"

                    else:
                        self.tela_config.modo_jogo = "AFK"
                    self.tela_config.modo_button.text = f"Modo: {self.tela_config.modo_jogo}"
                    
                if self.tela_config.fullscreen_button.handle_event(event):
                   self.tela_config.tela_cheia = not self.tela_config.tela_cheia

                   if self.tela_config.tela_cheia:
                       self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
                       self.tela_config.fullscreen_button.text = "Tela Cheia: ON"

                   else:
                       self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                       self.tela_config.fullscreen_button.text = "Tela Cheia: OFF"

            # GAMEPLAY
            elif self.current_state == "gameplay":

                self.gameplay.handle_events(event)

    def update(self):

        # GAMEPLAY
        if self.current_state == "gameplay":
            self.gameplay.update()
            
            if self.gameplay.sair_partida:
                self.parar_camera()
                
                pygame.display.quit()
                pygame.display.init()
                
                self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                pygame.display.set_caption("AFK")
                
                self.current_state = "pre_game"
                self.gameplay = None    

    def draw(self):
        
        #print(self.current_state)

        # MENU
        if self.current_state == "menu":
            self.tela_main.draw(self.screen)

        # PRE GAME
        elif self.current_state == "pre_game":
            self.pre_game.draw(self.screen)

        # GAMEPLAY
        elif self.current_state == "gameplay":
            self.gameplay.draw(self.screen)
        
        # TELA SKINS
        elif self.current_state == "skins":
            self.tela_skins.draw(self.screen)
            

        # TELA CONFIG
        elif self.current_state == "config":
            self.tela_config.draw(self.screen)
    