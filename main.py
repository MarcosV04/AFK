from multiprocessing import Process, Queue
from camera.hand_tracking import run_hand_tracking
from gamebase import jogo


def main():

    fila = Queue(maxsize=1)
    gestos = Queue(maxsize=1)
    config = Queue()

    processo_camera = Process(
        target=run_hand_tracking,
        args=(fila, config, gestos)
    )

    processo_jogo = Process(
        target=jogo,
        args=(fila, config, gestos)
    )

    print("Iniciando sistema...")

    processo_camera.start()
    processo_jogo.start()

    processo_camera.join()
    processo_jogo.join()


if __name__ == "__main__":
    main()