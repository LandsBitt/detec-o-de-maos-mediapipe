import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)

LARGURA_EXIBICAO = 800
ALTURA_EXIBICAO = int(LARGURA_EXIBICAO * 10 / 16)

ultimo_comando_tempo = 0
COOLDOWN_COMANDO = 1500
LIMITE_INDICADOR = 0.3
ultima_mao = None

COR_PONTOS = (128, 0, 128)
COR_LINHAS = (0, 255, 0)

with mp_maos.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.5) as maos:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (LARGURA_EXIBICAO, ALTURA_EXIBICAO), interpolation=cv2.INTER_AREA)

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = maos.process(frame_rgb)

        if resultados.multi_hand_landmarks:
            for pontos in resultados.multi_hand_landmarks:
                mp_desenho.draw_landmarks(
                    frame, pontos, mp_maos.HAND_CONNECTIONS,
                    mp_desenho.DrawingSpec(color=COR_PONTOS, thickness=2, circle_radius=3),
                    mp_desenho.DrawingSpec(color=COR_LINHAS, thickness=2)
                )

                indicador = pontos.landmark[mp_maos.HandLandmark.INDEX_FINGER_TIP]
                pulso = pontos.landmark[mp_maos.HandLandmark.WRIST]
                medio = pontos.landmark[mp_maos.HandLandmark.MIDDLE_FINGER_TIP]
                anelar = pontos.landmark[mp_maos.HandLandmark.RING_FINGER_TIP]
                mindinho = pontos.landmark[mp_maos.HandLandmark.PINKY_TIP]
                altura, largura, _ = frame.shape
                posicao_indicador_y = indicador.y * altura
                posicao_pulso_y = pulso.y * altura
                posicao_medio_y = medio.y * altura
                posicao_anelar_y = anelar.y * altura
                posicao_mindinho_y = mindinho.y * altura

                posicao_x_indicador = int(indicador.x * largura)
                posicao_y_indicador = int(indicador.y * altura)
                cv2.circle(frame, (posicao_x_indicador, posicao_y_indicador), 10, (0, 0, 255), -1)
                posicao_x_mindinho = int(mindinho.x * largura)
                posicao_y_mindinho = int(mindinho.y * altura)
                cv2.circle(frame, (posicao_x_mindinho, posicao_y_mindinho), 10, (0, 255, 0), -1)

                mao = resultados.multi_handedness[0].classification[0].label

                if ultima_mao != mao:
                    ultimo_comando_tempo = 0
                    ultima_mao = mao

                diferenca_indicador_y = posicao_indicador_y - posicao_pulso_y
                diferenca_mindinho_y = posicao_mindinho_y - posicao_pulso_y
                outros_dedos_abaixados = (posicao_medio_y > min(posicao_indicador_y, posicao_mindinho_y) and
                                        posicao_anelar_y > min(posicao_indicador_y, posicao_mindinho_y))

                tempo_atual = time.time() * 1000
                if tempo_atual - ultimo_comando_tempo >= COOLDOWN_COMANDO:
                    if mao == "Left":
                        if (abs(diferenca_indicador_y) > LIMITE_INDICADOR * altura and 
                            outros_dedos_abaixados and 
                            diferenca_indicador_y < 0):
                            print("Indicador (esquerda) detectado! Avançando slide...")
                            pyautogui.hotkey('right')
                            ultimo_comando_tempo = tempo_atual
                        elif (abs(diferenca_mindinho_y) > LIMITE_INDICADOR * altura and 
                              outros_dedos_abaixados and 
                              diferenca_mindinho_y < 0):
                            print("Mindinho (esquerda) detectado! Voltando slide...")
                            pyautogui.hotkey('left')
                            ultimo_comando_tempo = tempo_atual
                    elif mao == "Right":
                        if (abs(diferenca_indicador_y) > LIMITE_INDICADOR * altura and 
                            outros_dedos_abaixados and 
                            diferenca_indicador_y < 0):
                            print("Indicador (direita) detectado! Próxima faixa...")
                            pyautogui.hotkey('nexttrack')
                            ultimo_comando_tempo = tempo_atual
                        elif (abs(diferenca_mindinho_y) > LIMITE_INDICADOR * altura and 
                              outros_dedos_abaixados and 
                              diferenca_mindinho_y < 0):
                            print("Mindinho (direita) detectado! Faixa anterior...")
                            pyautogui.hotkey('prevtrack')
                            ultimo_comando_tempo = tempo_atual

        cv2.imshow("Mediapipe Mãos", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()