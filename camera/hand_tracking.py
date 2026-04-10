import cv2
import mediapipe as mp
import math

def run_hand_tracking():

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            print("Erro ao acessar a câmera")
            break

        img = cv2.flip(img, 1)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        h, w, _ = img.shape

        # Variável global
        movimento = "Parado"
        acao = "Parado"

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                label = results.multi_handedness[idx].classification[0].label

                cor = (0, 255, 0) if label == "Right" else (0, 0, 255)

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                pontos = []

                for lm in hand_landmarks.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    pontos.append((x, y))
                    cv2.circle(img, (x, y), 5, cor, -1)

                if len(pontos) != 21:
                    continue

                # Mao direita para movimentoção
                if label == "Right":
                    cx = pontos[0][0]
                    cy = pontos[0][1]

                    centro_x = w // 2
                    centro_y = h // 2

                    zona = 100  # Regulando ainda

                    if abs(cx - centro_x) < zona and abs(cy - centro_y) < zona:
                        movimento = "Parado"

                    elif cx < centro_x - zona:
                        movimento = "Esquerda"

                    elif cx > centro_x + zona:
                        movimento = "Direita"

                    elif cy < centro_y - zona:
                        movimento = "Frente"

                    elif cy > centro_y + zona:
                        movimento = "Tras"

                # Mao esquerda para acão
                if label == "Left":

                    dedos_levantados = []

                    polegar = pontos[4]
                    pulso = pontos[0]
                    base = pontos[5]

                    dist_polegar = math.hypot(polegar[0] - pulso[0], polegar[1] - pulso[1])
                    dist_base = math.hypot(base[0] - pulso[0], base[1] - pulso[1])

                    if dist_polegar > dist_base * 1.2:
                        dedos_levantados.append("Polegar")

                    if pontos[8][1] < pontos[6][1]:
                        dedos_levantados.append("Indicador")

                    if pontos[12][1] < pontos[10][1]:
                        dedos_levantados.append("Medio")

                    if pontos[16][1] < pontos[14][1]:
                        dedos_levantados.append("Anelar")

                    if pontos[20][1] < pontos[18][1]:
                        dedos_levantados.append("Mindinho")

                    if len(dedos_levantados) == 0:
                        acao = "Agachar"

                    elif "Indicador" in dedos_levantados:
                        acao = "Pular"

                    elif "Polegar" in dedos_levantados:
                        acao = "Especial"

                    else:
                        acao = "Parado"

        # Mostra na câmera o movimento e acão detectados
        cv2.putText(img, f"Movimento: {movimento}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(img, f"Acao: {acao}", (10, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.imshow("AFK - Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()