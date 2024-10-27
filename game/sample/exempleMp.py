import cv2
import mediapipe as mp

# Inizializzazione di MediaPipe Hands e degli strumenti di disegno
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Attivazione della videocamera e configurazione di MediaPipe Hands
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Conversione in RGB per MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Se rileva una mano, disegna i punti chiave
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Visualizzazione del frame con OpenCV
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()