import cv2
import mediapipe as mp
import time
from arduino_serial import send_command
import pyttsx3

# Inicializa e configura o sintetizador de voz
def init_tts():
    engine = pyttsx3.init()
    for v in engine.getProperty('voices'):
        langs = []
        for lang in v.languages:
            try:
                langs.append(lang.decode('utf-8').lower())
            except:
                langs.append(str(lang).lower())
        if any(l.startswith('pt') for l in langs) or 'brazil' in v.name.lower():
            engine.setProperty('voice', v.id)
            break
    return engine

engine = init_tts()

# Função de fala
def say(text):
    engine.say(text)
    engine.runAndWait()

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Comandos de dedo baseados em contagem
COMMANDS = {
    0: 'ALL_OFF',
    5: 'ALL_ON',
    1: 'BLUE_ON',
    2: 'RED_ON',
    3: 'GREEN_ON'
}

# Hold mínimo antes de aceitar o gesto
HOLD_TIME = 0.7  

def count_fingers(lm_list, frame_shape):
    h, w, _ = frame_shape
    tips_ids = [4, 8, 12, 16, 20]
    mcp_ids = [2, 5, 9, 13, 17]
    fingers = []

    # Calcular altura de referência da palma
    palm_height = abs(lm_list[0][1] - lm_list[9][1])

    # Polegar (comparar x)
    thumb_tip_x = lm_list[tips_ids[0]][0]
    thumb_base_x = lm_list[mcp_ids[0]][0]
    wrist_x = lm_list[0][0]
    if abs(thumb_tip_x - thumb_base_x) > 0.5 * palm_height:
        fingers.append(1)
    else:
        fingers.append(0)

    # Demais dedos (comparar y)
    for tip_id, mcp_id in zip(tips_ids[1:], mcp_ids[1:]):
        tip_y = lm_list[tip_id][1]
        mcp_y = lm_list[mcp_id][1]
        if mcp_y - tip_y > 0.2 * palm_height:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def main():
    say("Modo por gestos iniciado. Use indicador + mindinho (rock) para o tutorial falado.")
    hands = mp_hands.Hands(min_detection_confidence=0.7,
                           min_tracking_confidence=0.7)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        say("Não foi possível abrir a câmera.")
        return

    current_gesture = None
    gesture_start = 0
    last_action_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            fingers = None
            total = 0
            if results.multi_hand_landmarks:
                lm_list = [
                    (int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0]))
                    for lm in results.multi_hand_landmarks[0].landmark
                ]
                fingers = count_fingers(lm_list, frame.shape)
                total = sum(fingers)

                # Desenha na tela
                mp_draw.draw_landmarks(frame,
                                       results.multi_hand_landmarks[0],
                                       mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f"Fingers: {fingers}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.putText(frame, f"Count: {total}", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow('Hand Gesture Mode', frame)

            # Cooldown entre ações
            if now - last_action_time < 1.0:
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            # Detectar gestos especiais
            gesture = None
            # rock: indicador (1) + mindinho (4) levantados e somente eles
            if fingers and fingers[1] and fingers[4] and total == 2:
                gesture = 'rock'
            # exit: quatro dedos levantados sem polegar (índice, médio, anelar, mindinho)
            elif fingers and fingers[0] == 0 and sum(fingers[1:]) == 4:
                gesture = 'exit'
            # contagem: qualquer outro padrão válido
            elif fingers:
                gesture = 'count'

            # Se mudou de gesto, reinicia timer
            if gesture != current_gesture:
                current_gesture = gesture
                gesture_start = now

            # Se segurou tempo suficiente, dispara ação
            if gesture and now - gesture_start >= HOLD_TIME:
                if gesture == 'rock':
                    say("Ativando tutorial falado.")
                    say("Mão aberta com cinco dedos: liga tudo no Arduino.")
                    say("Mão fechada: desliga tudo.")
                    say("Apenas um dedo levantado: ativa o azul.")
                    say("Dois dedos levantados: ativa o vermelho.")
                    say("Três dedos levantados: ativa o verde.")
                    say("Quatro dedos, sem o polegar: sinal para sair do modo gestos.")
                elif gesture == 'exit':
                    say("Encerrando o modo de gestos.")
                    break
                elif gesture == 'count' and total in COMMANDS:
                    cmd = COMMANDS[total]
                    send_command(cmd)

                # prepara próximo gesto
                last_action_time = now
                current_gesture = None

            # Sair com Esc
            if cv2.waitKey(1) & 0xFF == 27:
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

    return "EXIT"

if __name__ == "__main__":
    main()
