import random
import cv2

class Bomb:
    def __init__(self):
        self.x = random.randint(50, 600)  # Posizione orizzontale iniziale
        self.y = 0                         # Inizio dall'alto dello schermo
        self.speed = random.randint(5, 10)  # Velocità di caduta
        self.is_cut = False                # Stato di taglio della frutta

    def update_position(self):
        if not self.is_cut:
            self.y += self.speed  # Aggiorna posizione (fa "cadere" la frutta)

    def check_collision(self, hand_position):
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            distance = ((hand_x - self.x) ** 2 + (hand_y - self.y) ** 2) ** 0.5
            return distance < 50  # Distanza limite per rilevare un taglio

    def draw(self, frame):
        if not self.is_cut:
            # Disegna un cerchio per rappresentare la bomba
            cv2.circle(frame, (self.x, self.y), 20, (55, 0, 255), -1)
