'''
from multiprocessing import Process, Queue
from camera.hand_tracking import run_hand_tracking
from game.game import jogo


def main():

    fila = Queue(maxsize=1)
    gestos = Queue(maxsize=1)
    config = Queue()

    processo_camera = Process(target=run_hand_tracking, args=(fila, config, gestos))

    processo_jogo = Process(target=jogo, args=(fila, config, gestos))

    print("Iniciando sistema...")

    processo_camera.start()
    processo_jogo.start()

    processo_camera.join()
    processo_jogo.join()


if __name__ == "__main__":
    main()
    
----------------/

import pygame

from jogo.states.main_menu.menu_inicial import MainMenu
from jogo.states.pre_game.pre_game import PreGame
from jogo.systems.skins import load_skin

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("AFK")

clock = pygame.time.Clock()

# states
main_menu = MainMenu(WIDTH, HEIGHT)
pre_game = PreGame(WIDTH, HEIGHT)

# state atual
current_state = "menu"

running = True

while running:

    for event in pygame.event.get():

        # fechar jogo
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # MENU PRINCIPAL
        if current_state == "menu":

            if main_menu.play_button.is_clicked(event): 
                current_state = "pre_game"

        # PRE GAME
        elif current_state == "pre_game":
            if pre_game.back_button.is_clicked(event):
                current_state = "menu"
            
            if pre_game.mode_button.is_clicked(event):
            
                if pre_game.selected_mode == "AFK":
                    pre_game.selected_mode = "TECLADO"
                else:
                    pre_game.selected_mode = "AFK"
                    
            if pre_game.skin_button.is_clicked(event):
                pre_game.current_skin += 1
                
                if pre_game.current_skin >= len(pre_game.skins):
                    pre_game.current_skin = 0

                pre_game.loaded_skin = load_skin(pre_game.skins[pre_game.current_skin])

                if pre_game.current_skin >= len(pre_game.skins):
                    pre_game.current_skin = 0

        pass

    # desenhar state atual
    if current_state == "menu":
        main_menu.draw(screen)

    elif current_state == "pre_game":
        pre_game.draw(screen)

    pygame.display.update()

    clock.tick(60)

pygame.quit()

'''

from core.game_manager import GameManager
from jogo.states.gameplay.game import game

if __name__ == "__main__":
    game = GameManager()
    game.run()