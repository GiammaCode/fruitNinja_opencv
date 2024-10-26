import random

class Fruit:
    def __init__(self):
        self.x = random.randint(0, 640)    # Posizione iniziale casuale sull'asse x
        self.y = 0                         # Partenza dall'alto
        self.is_cut = False

    def update_position(self):
        # Aggiorna la posizione per simulare la caduta
        pass
