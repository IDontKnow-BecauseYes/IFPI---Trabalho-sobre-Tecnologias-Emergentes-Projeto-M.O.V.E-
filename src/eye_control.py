import cv2
import mediapipe as mp
import numpy as np
import time

mp_face_mesh = mp.solutions.face_mesh

# Índices dos olhos (olho direito)
OLHO_INDICES = [33, 160, 158, 133, 153, 144]  # baseados nos landmarks do MediaPipe

def calcular_ear(landmarks, frame_w, frame_h):
    # EAR: eye aspect ratio
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

def olhar_direcao(landmarks, frame_w):
    olho_direito = [landmarks[33], landmarks[133]]
    iris = landmarks[468]
    olho_x = np.array([p.x for p in olho_direito]) * frame_w
    iris_x = iris.x * frame_w

    if iris_x < olho_x.mean() - 5:
        return "olhando para esquerda"
    elif iris_x > olho_x.mean() + 5:
        return "olhando para direita"
    else:
        return "olhando para frente"

def main():
    cap = cv2.VideoCapture(0)
    ear_limite = 0.2
    piscada_detectada = False
    contador_piscadas = 0
    confirmando_saida = False
    tempo_confirmacao = 0

    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
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

                direcao = olhar_direcao(landmarks, w)
                cv2.putText(frame, direcao, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                if ear < ear_limite:
                    if not piscada_detectada:
                        piscada_detectada = True
                        contador_piscadas += 1
                        print(f"PISCADA {contador_piscadas}")

                        if contador_piscadas == 2 and not confirmando_saida:
                            confirmando_saida = True
                            tempo_confirmacao = time.time()
                            contador_piscadas = 0
                            cv2.putText(frame, "Confirma saída com 2 piscadas", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
                            print("Aguardando confirmação de saída...")

                        elif contador_piscadas == 2 and confirmando_saida:
                            print("Saída confirmada.")
                            cap.release()
                            cv2.destroyAllWindows()
                            return "EXIT"

                else:
                    piscada_detectada = False

                # Tempo limite para confirmação
                if confirmando_saida and (time.time() - tempo_confirmacao > 3):
                    confirmando_saida = False
                    contador_piscadas = 0
                    print("Tempo de confirmação expirado. Cancelando saída.")

            cv2.imshow("Controle Ocular", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair (modo debug)
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
