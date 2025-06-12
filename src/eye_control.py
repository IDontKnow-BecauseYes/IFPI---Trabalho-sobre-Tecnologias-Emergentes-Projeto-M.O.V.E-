import cv2
import mediapipe as mp
import numpy as np
import time
import serial

mp_face_mesh = mp.solutions.face_mesh

# Índices dos olhos (olho direito)
OLHO_INDICES = [33, 160, 158, 133, 153, 144]

# Mapeamento de comandos por direção
EYE_COMMANDS = {
    "up": "ALL_ON",
    "down": "ALL_OFF",
    "right": ["BLUE_ON", "RED_ON", "GREEN_ON"],
    "left": ["GREEN_ON", "RED_ON", "BLUE_ON"]
}

# Porta do Arduino (ajuste conforme necessário)
try:
    arduino = serial.Serial('COM3', 9600)  # ou '/dev/ttyUSB0' no Linux
except:
    arduino = None
    print("Arduino não conectado.")

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

def main():
    print("Modo controle ocular ativado. Use seus olhos para enviar comandos.")
    cap = cv2.VideoCapture(0)
    ear_limite = 0.2
    piscada_detectada = False
    contador_piscadas = 0
    confirmando_saida = False
    tempo_confirmacao = 0

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5) as face_mesh:
        ultimo_comando = ""
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
                        print(f"PISCADA {contador_piscadas}")
                        if contador_piscadas == 2:
                            if confirmando_saida:
                                print("Saída confirmada.")
                                cap.release()
                                cv2.destroyAllWindows()
                                return "EXIT"
                            else:
                                confirmando_saida = True
                                tempo_confirmacao = time.time()
                                print("Aguardando confirmação de saída com mais 2 piscadas...")
                        elif confirmando_saida:
                            confirmando_saida = False
                else:
                    piscada_detectada = False

                if confirmando_saida and (time.time() - tempo_confirmacao > 3):
                    confirmando_saida = False
                    contador_piscadas = 0
                    print("Tempo de confirmação expirado. Cancelando saída.")

                if direcao in EYE_COMMANDS and direcao != ultimo_comando:
                    enviar_para_arduino(EYE_COMMANDS[direcao])
                    print(f"Comando ocular: {direcao.upper()} → {EYE_COMMANDS[direcao]}")
                    ultimo_comando = direcao

                cv2.putText(frame, f"Olhar: {direcao}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            cv2.imshow("Controle Ocular", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

