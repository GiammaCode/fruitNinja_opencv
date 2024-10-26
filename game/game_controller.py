import cv2
from game.hand_tracker import HandTracker
from game.fruit import Fruit
from game.score_manager import ScoreManager

class GameController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.score_manager = ScoreManager()
        self.fruits = []

    def spawn_fruit(self):
        fruit = Fruit()
        self.fruits.append(fruit)

    def detect_cut(self):
        # Logica per rilevare il taglio della frutta usando il tracciamento della mano
        pass

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Traccia la mano e disegna il frame
            self.hand_tracker.track(frame)

            # Aggiorna frutta e rileva tagli
            self.detect_cut()

            cv2.imshow("Fruit Ninja Game", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
