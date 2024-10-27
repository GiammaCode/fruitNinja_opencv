import cv2

class MenuScreen:
    def __init__(self):
        self.button_position = (250, 200)  # Posizione del pulsante "Start"
        self.button_size = (150, 100)      # Dimensione del pulsante

    def draw(self, frame):
        """Disegna il pulsante 'Start' al centro del frame."""
        x, y = self.button_position
        w, h = self.button_size
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
        cv2.putText(frame, "START", (x + 20, y + 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    def check_start(self, hand_position):
        """Controlla se la mano è sopra il pulsante 'Start'."""
        x, y = self.button_position
        w, h = self.button_size
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            return x <= hand_x <= x + w and y <= hand_y <= y + h
        return False
