import cv2
import mediapipe as mp
import math  # 🔥 necessário para cálculo de distância

def run_hand_tracking():

    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7)

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

        if results.multi_hand_landmarks and results.multi_handedness:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

                label = results.multi_handedness[idx].classification[0].label

                cor = (255, 0, 0) if label == "Right" else (0, 0, 255)
                y_texto = 50 if label == "Right" else 100

                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                pontos = []

                for lm in hand_landmarks.landmark:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    pontos.append((x, y))
                    cv2.circle(img, (x, y), 5, cor, -1)

                if len(pontos) == 21:
                    dedos_levantados = []

                    # 🔥 POLEGAR (VERSÃO ROBUSTA)
                    polegar = pontos[4]
                    indicador_base = pontos[5]
                    pulso = pontos[0]

                    dist_polegar_pulso = math.hypot(polegar[0] - pulso[0], polegar[1] - pulso[1])

                    dist_base = math.hypot(indicador_base[0] - pulso[0], indicador_base[1] - pulso[1])

                    if dist_polegar_pulso > dist_base * 1.2:
                        dedos_levantados.append("Polegar")

                    # OUTROS DEDOS
                    if pontos[8][1] < pontos[6][1]:
                        dedos_levantados.append("Indicador")

                    if pontos[12][1] < pontos[10][1]:
                        dedos_levantados.append("Medio")

                    if pontos[16][1] < pontos[14][1]:
                        dedos_levantados.append("Anelar")

                    if pontos[20][1] < pontos[18][1]:
                        dedos_levantados.append("Mindinho")

                    cv2.putText(img, f"{label}: {dedos_levantados}", (10, y_texto), cv2.FONT_HERSHEY_SIMPLEX,0.7,cor,2)
                    
        cv2.imshow("AFK - Hand Tracking", img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()