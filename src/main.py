import cv2
import mediapipe as mp
import time
import speech_recognition as sr
import pyttsx3
import arduino_serial
import hand_gesture

# Inicializa engine de voz
engine = pyttsx3.init()
# Seleciona voz feminina (pt-BR)
for v in engine.getProperty('voices'):
    if 'pt' in v.languages or 'Maria' in v.name:
        engine.setProperty('voice', v.id)
        break

# Função para falar
def say(text):
    engine.say(text)
    engine.runAndWait()

# Função para detectar número de dedos usando MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Introdução
say("Este programa ativa modos por gesto de mão e conexão Arduino.")

zero_time = None

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    last_detect_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        finger_count = None
        if results.multi_hand_landmarks:
            last_detect_time = time.time()
            hand_landmarks = results.multi_hand_landmarks[0]
            tips = [4, 8, 12, 16, 20]
            count = 0
            for tip in tips:
                finger_tip = hand_landmarks.landmark[tip]
                finger_dip = hand_landmarks.landmark[tip - 2]
                if finger_tip.y < finger_dip.y:
                    count += 1
            finger_count = count

        # Se não detectar mão por mais de 2 segundos, continua o loop
        if finger_count is None and time.time() - last_detect_time > 2:
            continue

        if finger_count == 4:
            saida = arduino_serial.check_connection()
            if saida:
                say("Arduino está conectado ao PC.")
            else:
                say("Arduino não está conectado ao PC.")
            time.sleep(1)
            continue

        if finger_count == 5:
            resultado = hand_gesture.main()
            if resultado == "EXIT":
                say("Retornando ao modo principal após encerramento do modo de gestos.")
            time.sleep(1)
            continue

        if finger_count == 0:
            now = time.time()
            if zero_time is None:
                zero_time = now
                say("Deseja encerrar o programa? Levante zero dedos novamente em até 2 segundos para confirmar.")
            else:
                if now - zero_time <= 2:
                    say("Encerrando o programa. Até mais!")
                    break
                else:
                    zero_time = None
            time.sleep(1)
            continue

        # Redefine zero_time se qualquer outro gesto
        zero_time = None

        # Exibe frame com desenho de mãos (opcional)
        if results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('Hand Gesture Control', frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair manual
            break

cap.release()
cv2.destroyAllWindows()

