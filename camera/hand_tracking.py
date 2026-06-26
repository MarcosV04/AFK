import cv2
import mediapipe as mp


from multiprocessing import Queue

def run_hand_tracking(fila, config, gestos):

    # Inicializa MediaPipe
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

    # Webcam
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("Erro ao abrir câmera")
        return

    print("Câmera iniciada!")
    
    ultima_mao = ""
    
    try:

        while True:
        
            sucesso, frame = cap.read()
    
            if not sucesso:
                print("Erro ao ler frame")
                break
            
            # Espelha imagem
            frame = cv2.flip(frame, 1)
    
            altura, largura, _ = frame.shape
    
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
            frame_rgb.flags.writeable = False
            
            resultado = hands.process(frame_rgb)
            
            frame_rgb.flags.writeable = True
    
            pontos = []
            pontos_gesto = []
            acao = "Parado"
    
            if resultado.multi_hand_landmarks and resultado.multi_handedness:
            
                # IDENTIFICA AS MÃOS
                for idx, hand_info in enumerate(resultado.multi_handedness):
                
                    label = hand_info.classification[0].label
                    hand_landmarks = resultado.multi_hand_landmarks[idx]
                    
                    # DESENHA TODAS AS MÃOS
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # COLETA PONTOS
                    pontos_temp = []
                    for lm in hand_landmarks.landmark:
                    
                        x = int(lm.x * largura)
                        y = int(lm.y * altura)
                        pontos_temp.append((x, y))
                        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                        
                    # ESCOLHE MÃO DE CONTROLE
                    #if label == ultima_mao or len(pontos) == 0:
                    
                        # CORRIGE ESPELHAMENTO DA MÃO ESQUERDA
                        #if label == "Left":
                        
                            #pontos_temp[4], pontos_temp[20] = pontos_temp[20], pontos_temp[4]
                            #pontos_temp[8], pontos_temp[16] = pontos_temp[16], pontos_temp[8]
                    
                        #pontos = pontos_temp
    
                    #else:
                    
                        #pontos_gesto = pontos_temp
                    if len(pontos) == 0:

                        pontos = pontos_temp
                    
                    else:
                    
                        pontos_gesto = pontos_temp
                        
                    if len(pontos) < 21 and len(pontos_gesto) >= 21:
                    
                        pontos = pontos_gesto
                        
                # GESTOS DA MÃO ESQUERDA REAL
                if len(pontos_gesto) >= 21:
                
                    if pontos_gesto[8][1] < pontos_gesto[6][1]:
                    
                        acao = "Pular"
                    else:
                    
                        acao = "Agachar"
    
            # Atualiza fila de pontos
            if len(pontos) >= 21:
            
                if fila is not None:
                
                    try:
                    
                        if fila.full():
                            fila.get_nowait()
                
                        # ENVIA SOMENTE SE TIVER MÃO
                        if len(pontos) >= 21:
                        
                            fila.put_nowait(pontos)
        
                        else:
                        
                            fila.put_nowait([])
                
                    except Exception as erro:
                        print("Erro fila:", erro)
    
            # Atualiza fila de gestos
            if gestos is not None:
            
                try:
                    if gestos.full():
                        gestos.get_nowait()
                    gestos.put_nowait(acao)
    
                except:
                    pass
                
            # Mostrar ação
            cv2.putText(
                frame, f"Acao: {acao}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
            pass
        
            cv2.imshow("AFK - Camera", frame)
        
            tecla = cv2.waitKey(1)
    
            # ESC fecha
            if tecla == 27:
                break
    
            # Comunicação de fechamento
            if config is not None and not config.empty():
            
                comando = config.get()
    
                if comando == "Fechar":
                    break
                
    except Exception as erro:
        print("ERRO NO HAND TRACKING:", erro)
    
    finally:

        print("Finalizando processo da câmera...")
    
        try:
            hands.close()
        except:
            pass
        
        try:
            if cap.isOpened():
                cap.release()
        except:
            pass
        
        # COMENTA ESSA LINHA
        # cv2.destroyAllWindows()
    
        print("Câmera finalizada!")
    
    if __name__ == "__main__":
    
        fila = Queue()
        config = Queue()
        gestos = Queue()
    
        run_hand_tracking(fila, config, gestos)