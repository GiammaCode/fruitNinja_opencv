import cv2
import time


class MenuScreen:
    def __init__(self):
        self.button_position = (250, 200)  # Posizione del pulsante "Start"
        self.button_size = (150, 100)  # Dimensione del pulsante
        self.last_pulse_time = time.time()  # Ultimo tempo di pulsazione
        self.pulse = False  # Stato di pulsazione

    def draw_rounded_rectangle(self, frame, top_left, bottom_right, color, radius=20, thickness=-1):
        """Disegna un rettangolo stondato."""
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Disegna i cerchi per gli angoli
        cv2.circle(frame, (x1 + radius, y1 + radius), radius, color, thickness)
        cv2.circle(frame, (x2 - radius, y1 + radius), radius, color, thickness)
        cv2.circle(frame, (x1 + radius, y2 - radius), radius, color, thickness)
        cv2.circle(frame, (x2 - radius, y2 - radius), radius, color, thickness)

        # Disegna i rettangoli tra i cerchi
        cv2.rectangle(frame, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
        cv2.rectangle(frame, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    def draw(self, frame):
        font = cv2.FONT_HERSHEY_TRIPLEX
        score_text = f"FRUIT NINJA"
        cv2.putText(frame, score_text, (100, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

        """Disegna il pulsante 'Start' con effetto di pulsazione e bordi stondati."""
        current_time = time.time()

        # Alterna lo stato di pulsazione ogni 0.5 secondi
        if current_time - self.last_pulse_time >= 0.5:
            self.pulse = not self.pulse
            self.last_pulse_time = current_time

        # Cambia il colore del pulsante durante la pulsazione
        button_color = (0, 200, 0) if self.pulse else (0, 255, 0)

        # Determina la posizione e le dimensioni del pulsante
        x, y = self.button_position
        w, h = self.button_size

        # Disegna il rettangolo stondato per il pulsante "Start"
        self.draw_rounded_rectangle(frame, (x, y), (x + w, y + h), button_color, radius=20, thickness=-1)

        # Disegna il testo "START" al centro del pulsante
        text_size, _ = cv2.getTextSize("START", font, 1, 2)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(frame, "START", (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    def check_start(self, hand_position):
        """Controlla se la mano è sopra il pulsante 'Start'."""
        x, y = self.button_position
        w, h = self.button_size
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            return x <= hand_x <= x + w and y <= hand_y <= y + h
        return False
