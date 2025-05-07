import cv2
import mediapipe as mp

# Inicializa o MediaPipe para detectar as mãos
mp_maos = mp.solutions.hands
maos = mp_maos.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.5)
mp_desenho = mp.solutions.drawing_utils

# Inicializa a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    # Lê o frame da câmera
    ret, frame = cap.read()
    if not ret:
        print("Falha na captura de vídeo!")
        break

    # Converte a imagem para RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processa o frame com o modelo de mãos
    resultados = maos.process(frame_rgb)

    # Se mãos forem detectadas, desenha as conexões
    if resultados.multi_hand_landmarks:
        for pontos in resultados.multi_hand_landmarks:
            mp_desenho.draw_landmarks(frame, pontos, mp_maos.HAND_CONNECTIONS)

    # Exibe o frame com as mãos detectadas
    cv2.imshow("Mediapipe Mãos", frame)

    # Sai do loop ao apertar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()