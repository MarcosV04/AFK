import pygame

from multiprocessing import Process, Queue
from jogo.states.tela_main.menu_inicial import menu
from jogo.states.tela_pre_game.pre_game import PreGame
from jogo.states.gameplay.game import game
from jogo.systems.skins import load_skin
from camera.hand_tracking import run_hand_tracking
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
        self.gameplay = None

        # STATE ATUAL
        self.current_state = "menu"
        self.running = True

    def iniciar_camera(self):

        if self.camera_process is None:
            self.camera_process = Process(
                target=run_hand_tracking,
                args=(self.fila, self.config, self.gestos))
            self.camera_process.start()

    def run(self):

        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(60)
            pygame.display.update()
        
        pygame.quit()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            # MENU PRINCIPAL
            if self.current_state == "menu":
                if self.tela_main.handle_events(event):
                    self.current_state = "pre_game"

            # PRE GAME
            elif self.current_state == "pre_game":
                if self.pre_game.back_button.is_clicked(event):
                    self.current_state = "menu"

                # TROCAR MODO
                if self.pre_game.mode_button.is_clicked(event):
                    if self.pre_game.selected_mode == "AFK":
                        self.pre_game.selected_mode = "TECLADO"
                    else:
                        self.pre_game.selected_mode = "AFK"

                # TROCAR SKIN
                if self.pre_game.skin_button.is_clicked(event):
                    self.pre_game.current_skin += 1
                    if (self.pre_game.current_skin >= len(self.pre_game.skins)):
                        self.pre_game.current_skin = 0
                    self.pre_game.loaded_skin = load_skin(
                        self.pre_game.skins[self.pre_game.current_skin])

                # INICIAR JOGO
                if self.pre_game.start_button.is_clicked(event):
                    self.iniciar_camera()
                    skin_escolhida = (self.pre_game.skins[self.pre_game.current_skin])
                    self.gameplay = game(self.WIDTH, self.HEIGHT, self.fila, self.config, self.gestos, skin_escolhida)
                    self.current_state = "gameplay"

            # GAMEPLAY
            elif self.current_state == "gameplay":
                self.gameplay.handle_events(event)

    def update(self):

        # GAMEPLAY
        if self.current_state == "gameplay":
            self.gameplay.update()

    def draw(self):

        # MENU
        if self.current_state == "menu":
            self.tela_main.draw(self.screen)

        # PRE GAME
        elif self.current_state == "pre_game":
            self.pre_game.draw(self.screen)

        # GAMEPLAY
        elif self.current_state == "gameplay":
            self.gameplay.draw(self.screen)