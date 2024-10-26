# game/game_controller.py
import cv2
from game.hand_tracker import HandTracker
from game.fruit import Fruit
from game.score_manager import ScoreManager
import random

class GameController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.score_manager = ScoreManager()
        self.fruits = []
        self.frames_since_last_spawn = 0

    def spawn_fruit(self):
        fruit = Fruit()
        self.fruits.append(fruit)

    def detect_cut(self, hand_position):
        for fruit in self.fruits:
            if not fruit.is_cut and fruit.check_collision(hand_position):
                fruit.is_cut = True
                self.score_manager.update_score(10)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)

            hand_position = self.hand_tracker.track(frame)

            # Genera nuova frutta ogni 50 fotogrammi
            self.frames_since_last_spawn += 1
            if self.frames_since_last_spawn > 50:
                self.spawn_fruit()
                self.frames_since_last_spawn = 0

            for fruit in self.fruits:
                fruit.update_position()
                if not fruit.is_cut:
                    fruit.draw(frame)

            if hand_position:
                self.detect_cut(hand_position)

            cv2.imshow("Fruit Ninja Game", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
