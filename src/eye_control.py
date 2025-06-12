import cv2
import mediapipe as mp
import numpy as np
import time
import serial
import pyttsx3

mp_face_mesh = mp.solutions.face_mesh
OLHO_INDICES = [33, 160, 158, 133, 153, 144]

EYE_COMMANDS = {
    "up": "ALL_ON",
    "down": "ALL_OFF",
    "right": ["BLUE_ON", "RED_ON", "GREEN_ON"],
    "left": ["GREEN_ON", "RED_ON", "BLUE_ON"]
}

# Arduino
try:
    arduino = serial.Serial('COM3', 9600)  # Ajuste se necessário
except:
    arduino = None
    print("Arduino não conectado.")

# Voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 170)

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def calcular_ear(landmarks, frame_w, frame_h):
    p2 = np.array([landmarks[160].x * frame_w, landmarks[160].y * frame_h])
    p6 = np.array([landmarks[144].x * frame_w, landmarks[144].y * frame_h])
    p3 = np.array([landmarks[158].x * frame_w, landmarks[158].y * frame_h])
    p5 = np.array([landmarks[153].x * frame_w, landmarks[153].y * frame_h])
    p1 = np.array([landmarks[33].x * frame_w, landmarks[33].y * frame_h])
    p4 = np.array([landmarks[133].x * frame_w, landmarks[133].y * frame_h])
    vertical1 = np.linalg.norm(p2 - p6)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

def detectar_direcao(landmarks, frame_w, frame_h):
    iris = landmarks[468]
    olho_direito = [landmarks[33], landmarks[133]]
    iris_x = iris.x * frame_w
    iris_y = iris.y * frame_h
    olho_x = np.array([p.x for p in olho_direito]) * frame_w
    centro_x = olho_x.mean()

    if iris_y < frame_h * 0.35:
        return "up"
    elif iris_y > frame_h * 0.65:
        return "down"
    elif iris_x < centro_x - 15:
        return "left"
    elif iris_x > centro_x + 15:
        return "right"
    return "center"

def enviar_para_arduino(comando):
    if arduino:
        if isinstance(comando, list):
            for cmd in comando:
                arduino.write((cmd + '\n').encode())
                time.sleep(1)
        else:
            arduino.write((comando + '\n').encode())
            time.sleep(1)

def tutorial():
    falas = [
        "Bem-vindo ao controle ocular.",
        "Olhe para cima para ligar todas as luzes.",
        "Olhe para baixo para desligar todas as luzes.",
        "Olhe para a direita para acender uma luz de cada vez.",
        "Olhe para a esquerda para acender uma luz por vez na ordem inversa.",
        "Para sair, pisque duas vezes e depois mais duas vezes para confirmar."
    ]
    for frase in falas:
        falar(frase)
        time.sleep(1)

def main():
    print("Modo ocular iniciado.")
    tutorial()
    cap = cv2.VideoCapture(0)
    ear_limite = 0.2
    piscada_detectada = False
    contador_piscadas = 0
    confirmando_saida = False
    tempo_confirmacao = 0
    ultimo_comando = ""

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5) as face_mesh:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(frame_rgb)
            h, w, _ = frame.shape

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                ear = calcular_ear(landmarks, w, h)
                direcao = detectar_direcao(landmarks, w, h)

                if ear < ear_limite:
                    if not piscada_detectada:
                        piscada_detectada = True
                        contador_piscadas += 1
                        if contador_piscadas == 2:
                            if confirmando_saida:
                                falar("Saindo do controle ocular.")
                                cap.release()
                                cv2.destroyAllWindows()
                                return "EXIT"
                            else:
                                confirmando_saida = True
                                tempo_confirmacao = time.time()
                                falar("Deseja sair? Pisque mais duas vezes.")
                else:
                    piscada_detectada = False

                if confirmando_saida and (time.time() - tempo_confirmacao > 3):
                    confirmando_saida = False
                    contador_piscadas = 0
                    falar("Tempo de confirmação esgotado.")

                if direcao in EYE_COMMANDS and direcao != ultimo_comando:
                    enviar_para_arduino(EYE_COMMANDS[direcao])
                    if direcao == "up":
                        falar("Luzes ligadas")
                    elif direcao == "down":
                        falar("Luzes desligadas")
                    elif direcao == "right":
                        falar("Sequência da direita")
                    elif direcao == "left":
                        falar("Sequência da esquerda")
                    ultimo_comando = direcao

                cv2.putText(frame, f"Olhar: {direcao}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Controle Ocular", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
