import cv2
import mediapipe as mp
from arduino_serial import send_command
import speech_recognition as sr
import pyttsx3

# Configurando a voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "brazil" in voice.name.lower() or "pt" in voice.id.lower():
        engine.setProperty('voice', voice.id)
        break

def say(text):
    engine.say(text)
    engine.runAndWait()

# MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Comandos de dedo
COMMANDS = {
    0: 'ALL_OFF',
    5: 'ALL_ON',
    1: 'BLUE_ON',
    2: 'RED_ON',
    3: 'GREEN_ON'
}

def ouvir_comando():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Aguardando comando de voz...")
        audio = recognizer.listen(source)
    try:
        frase = recognizer.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {frase}")
        if "lira" in frase:
            say("Estou ouvindo")
            if "tutorial" in frase:
                say("Modo por gestos ativado por Lira. Aqui está o tutorial.")
                say("Mão aberta com cinco dedos: liga tudo.")
                say("Mão fechada: desliga tudo.")
                say("Apenas um dedo: ativa o azul.")
                say("Dois dedos: ativa o vermelho.")
                say("Três dedos: ativa o verde.")
                say("Quatro dedos, sem o polegar: sinal para encerrar o modo de gestos.")
    except Exception as e:
        print("Erro no reconhecimento de voz:", e)

def main():
    ouvir_comando()  # Escuta logo no início

    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                fingers = []
                tips_ids = [4, 8, 12, 16, 20]
                lm_list = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, _ = frame.shape
                    lm_list.append((int(lm.x * w), int(lm.y * h)))
                # Polegar
                if lm_list[tips_ids[0]][0] < lm_list[tips_ids[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # Outros dedos
                for id in range(1, 5):
                    if lm_list[tips_ids[id]][1] < lm_list[tips_ids[id] - 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = sum(fingers)

                # Gesto de encerrar
                if fingers == [0, 1, 1, 1, 1]:
                    say("Sinal de encerrar detectado. Saindo do modo de gestos.")
                    cap.release()
                    cv2.destroyAllWindows()
                    return "EXIT"

                cmd = COMMANDS.get(total_fingers)
                if cmd:
                    send_command(cmd)

                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('M.O.V.E Gesture Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
