# game/game_controller.py
import cv2

from game.bomb import Bomb
from game.fruit import Fruit
from game.hand_tracker import HandTracker
from game.score_manager import ScoreManager


class GameController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.score_manager = ScoreManager()
        self.fruits = []
        self.bombs = []
        self.frames_since_last_fruit_spawn = 0
        self.frames_since_last_bomb_spawn = 0

    def spawn_fruit(self):
        fruit = Fruit()
        self.fruits.append(fruit)

    def spawn_bomb(self):
        bomb = Bomb()
        self.bombs.append(bomb)

    def detect_cut_fruit(self, hand_position):
        for fruit in self.fruits:
            if not fruit.is_cut and fruit.check_collision(hand_position):
                fruit.is_cut = True
                self.score_manager.update_score(10)

    def detect_cut_bomb(self, hand_position):
        for bomb in self.bombs:
            if not bomb.is_cut and bomb.check_collision(hand_position):
                bomb.is_cut = True
                # self.score_manager.update_score(10)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # flipped mirror image
            frame = cv2.flip(frame, 1)

            hand_position = self.hand_tracker.track(frame)

            # Genera nuova frutta ogni 50 fotogrammi
            self.frames_since_last_fruit_spawn += 1
            if self.frames_since_last_fruit_spawn > 40:
                #print("spawn fruit")
                self.spawn_fruit()
                self.frames_since_last_fruit_spawn = 0

            # genero bomba ogni 60 fotogrammi
            self.frames_since_last_bomb_spawn += 1
            if self.frames_since_last_bomb_spawn > 60:
                self.spawn_bomb()
                self.frames_since_last_bomb_spawn = 0

            for bomb in self.bombs:
                bomb.update_position()
                if not bomb.is_cut:
                    bomb.draw(frame)

            for fruit in self.fruits:
                fruit.update_position()
                if not fruit.is_cut:
                    fruit.draw(frame)

            if hand_position:
                self.detect_cut_fruit(hand_position)
                self.detect_cut_bomb(hand_position)

            cv2.imshow("Fruit Ninja Game", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
