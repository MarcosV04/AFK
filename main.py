from multiprocessing import Process, Queue
from camera.hand_tracking import run_hand_tracking
from gamebase import jogo

def main():
    # A fila (Queue) é o "cano" por onde os dados da câmera vão para o jogo
    fila = Queue()

    # Criamos os processos independentes
    # 'args=(fila,)' passa a caixa de mensagens para as funções
    processo_camera = Process(target=run_hand_tracking, args=(fila,))
    processo_jogo = Process(target=jogo, args=(fila,))

    print("Iniciando Hand Tracking e Jogo...")
    processo_camera.start()
    processo_jogo.start()

    # Mantém o script rodando enquanto os processos estiverem vivos
    processo_camera.join()
    processo_jogo.join()

if __name__ == "__main__":
    main()
