import cv2
import mediapipe as mp
import time
import pyttsx3
import arduino_serial
import hand_gesture

# Inicializa engine de voz
engine = pyttsx3.init()
# Seleciona voz feminina (pt-BR)
for v in engine.getProperty('voices'):
    langs = []
    try:
        langs = [lang.decode('utf-8').lower() for lang in v.languages]
    except:
        langs = [str(lang).lower() for lang in v.languages]
    if any(lang.startswith('pt') for lang in langs) or 'maria' in v.name.lower():
        engine.setProperty('voice', v.id)
        break

def say(text):
    engine.say(text)
    engine.runAndWait()

# Configuração MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Não foi possível abrir a câmera")

say("Introdução aqui:")

start_time = time.time()
reaction_delay = 1.5  # segundos de espera antes de reconhecer gestos

# Estados para detecção de hold
current_action = None
gesture_start = None
hold_time = 0.7          # segundos para manter o gesto
last_action_time = 0     # timestamp da última ação concluída

try:
    with mp_hands.Hands(min_detection_confidence=0.7,
                        min_tracking_confidence=0.7) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            finger_count = 0
            if results.multi_hand_landmarks:
                lm = results.multi_hand_landmarks[0].landmark
                # altura da mão (ponto 0 = punho, 9 = meio da mão)
                hand_height = abs(lm[0].y - lm[9].y)
                # quatro dedos (exclui polegar)
                tips = [8, 12, 16, 20]
                bases = [5, 9, 13, 17]
                for tip, base in zip(tips, bases):
                    if lm[tip].y < lm[base].y - 0.03 * hand_height:
                        finger_count += 1
                # polegar
                if abs(lm[4].x - lm[2].x) > 0.5 * hand_height:
                    finger_count += 1

            # Desenha landmarks em cópia do frame
            annotated = frame.copy()
            if results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(annotated,
                                          results.multi_hand_landmarks[0],
                                          mp_hands.HAND_CONNECTIONS)
            cv2.putText(annotated, f'Dedos: {finger_count}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Drusa Control', annotated)

            # espaçamento inicial antes de começar a ler gestos
            if now - start_time < reaction_delay:
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            # evita reagir muito rápido após uma ação
            if now - last_action_time < 1.0:
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                continue

            # define ação com base na contagem de dedos
            action = None
            if results.multi_hand_landmarks:
                if finger_count == 5:
                    action = 'hand_mode'
                elif finger_count == 3:
                    action = 'check_conn'
                elif finger_count == 0:
                    action = 'exit'

            # reseta estado se gesto ficou em None
            if action is None:
                current_action = None
            # gestos novos
            elif action != current_action:
                current_action = action
                gesture_start = now
            # tempo de espera
            elif now - gesture_start >= hold_time:
                if action == 'check_conn':
                    ok = arduino_serial.check_connection()
                    say("Arduino conectado." if ok else "Arduino não conectado.")
                elif action == 'hand_mode':
                    cap.release()
                    try:
                        hand_gesture.main()
                    finally:
                        cap = cv2.VideoCapture(0)
                        if not cap.isOpened():
                            say("Erro ao reabrir a câmera!")
                            break
                        start_time = time.time()
                        say("Retornando ao modo principal.")
                elif action == 'exit':
                    say("Encerrando o programa. Até mais!")
                    break

                last_action_time = now
                current_action = None
                gesture_start = None

            # em caso de ma função, botão esc encerra o programa
            if cv2.waitKey(1) & 0xFF == 27:
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
