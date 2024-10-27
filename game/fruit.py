import random
import cv2
import time


class Fruit:
    def __init__(self):
        # Carica le immagini del frutto e della versione tagliata
        self.image = cv2.imread("C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/apple.png",
                                cv2.IMREAD_UNCHANGED)  # Usa un percorso corretto per apple.png

        self.x = random.randint(50, 600)  # Posizione orizzontale iniziale
        self.y = 0  # Inizio dall'alto dello schermo
        self.speed = random.randint(5, 10)  # Velocità di caduta
        self.is_cut = False  # Stato di taglio della frutta
        self.cut_time = None  # Timestamp del taglio

    def update_position(self):
        if not self.is_cut:
            self.y += self.speed  # Aggiorna posizione (fa "cadere" la frutta)

    def check_collision(self, hand_position):
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            distance = ((hand_x - self.x) ** 2 + (hand_y - self.y) ** 2) ** 0.5
            return distance < 50  # Distanza limite per rilevare un taglio

    def draw(self, frame):
        """
        Sovrappone l'immagine del frutto al frame alla posizione (self.x, self.y),
        gestendo la trasparenza se l'immagine ha un canale alpha.

        :param frame: Il frame della videocamera su cui disegnare l'immagine.
        """
        h, w, _ = self.image.shape  # Ottieni altezza e larghezza dell'immagine del frutto
        # Controlla che l'immagine non esca dai bordi del frame
        if self.y + h >= frame.shape[0] or self.x + w >= frame.shape[1]:
            return

        # Estrai il canale alpha dell'immagine per gestire la trasparenza
        alpha_s = self.image[:, :, 3] / 255.0  # Canale alpha normalizzato
        alpha_l = 1.0 - alpha_s  # Trasparenza inversa per il frame di background

        # Sovrapponi i canali BGR dell'immagine del frutto sul frame
        for c in range(3):  # Ciclo sui canali BGR
            frame[self.y:self.y + h, self.x:self.x + w, c] = (
                    alpha_s * self.image[:, :, c] +  # Pixel del frutto con trasparenza
                    alpha_l * frame[self.y:self.y + h, self.x:self.x + w, c]  # Pixel del frame di background
            )
