import cv2
import mediapipe as mp

# Inicializa MediaPipe
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

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = img.shape

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):

            # Detecta se é direita ou esquerda
            label = results.multi_handedness[idx].classification[0].label

            # Define cor
            if label == "Right":
                cor = (255, 0, 0)  # Vermelho
                y_texto = 50
            else:
                cor = (0, 0, 255)  # Azul
                y_texto = 100

            # Desenha mão
            mp_drawing.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            pontos = []

            for id, lm in enumerate(hand_landmarks.landmark):
                x = int(lm.x * w)
                y = int(lm.y * h)

                pontos.append((x, y))
                cv2.circle(img, (x, y), 5, cor, -1)

            if len(pontos) == 21:

                dedos_levantados = []

                if pontos[8][1] < pontos[6][1]:
                    dedos_levantados.append("Indicador")

                if pontos[12][1] < pontos[10][1]:
                    dedos_levantados.append("Medio")

                if pontos[16][1] < pontos[14][1]:
                    dedos_levantados.append("Anelar")

                if pontos[20][1] < pontos[18][1]:
                    dedos_levantados.append("Mindinho")

                if pontos[4][0] < pontos[3][0]:
                    dedos_levantados.append("Polegar")

                # Mostra na tela com cor e posição separada
                cv2.putText(img,
                            f"{label}: {dedos_levantados}",
                            (10, y_texto), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 255, 0),2)
                            
    cv2.imshow("AFK - Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()