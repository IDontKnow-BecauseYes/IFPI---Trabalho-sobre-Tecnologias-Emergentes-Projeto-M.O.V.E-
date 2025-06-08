import cv2
import mediapipe as mp
from arduino_serial import send_command

# Inicializa MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Mapeia número de dedos a comandos
COMMANDS = {
    0: 'ALL_OFF',   # mão fechada
    5: 'ALL_ON',    # mão aberta (5 dedos)
    1: 'BLUE_ON',
    2: 'RED_ON',
    3: 'GREEN_ON'
}

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
            # Conta dedos levantados
            tips_ids = [4, 8, 12, 16, 20]
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = frame.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))
            # Verifica polegar
            if lm_list[tips_ids[0]][0] < lm_list[tips_ids[0] - 1][0]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Demais dedos
            for id in range(1, 5):
                if lm_list[tips_ids[id]][1] < lm_list[tips_ids[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total_fingers = sum(fingers)
            # Seleciona comando
            cmd = COMMANDS.get(total_fingers)
            if cmd:
                send_command(cmd)
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('M.O.V.E Gesture Control', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
