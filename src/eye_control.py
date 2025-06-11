import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

# Função para calcular a posição horizontal do olhar
def olhar_direcao(landmarks, frame_w):
    # Pegamos dois pontos na pálpebra direita para medir o olhar (exemplo simplificado)
    olho_direito = [landmarks[33], landmarks[133]]  # pontos do olho direito na face mesh
    # Pegamos o ponto da íris (aprox. no meio do olho direito)
    iris = landmarks[468]  # ponto da íris
    
    # Coordenadas normalizadas (0-1), vamos para pixel
    olho_x = np.array([p.x for p in olho_direito]) * frame_w
    iris_x = iris.x * frame_w
    
    # Se o iris está mais para esquerda dentro do olho -> olhando para esquerda
    # Se está mais para direita dentro do olho -> olhando para direita
    if iris_x < olho_x.mean() - 5:
        return "olhando para esquerda"
    elif iris_x > olho_x.mean() + 5:
        return "olhando para direita"
    else:
        return "olhando para frente"

cap = cv2.VideoCapture(0)

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
        
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            h, w, _ = frame.shape
            
            direcao = olhar_direcao(landmarks, w)
            
            cv2.putText(frame, direcao, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        
        cv2.imshow("Controle Ocular", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
            break

cap.release()
cv2.destroyAllWindows()

