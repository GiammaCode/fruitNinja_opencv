import cv2
from game.entities.bomb import Bomb
from game.entities.fruit import Fruit
from game.utils.hand_tracker import HandTracker
from game.screen.loseScreen import LoseScreen
from game.screen.menuScreen import MenuScreen
from game.utils.score_manager import ScoreManager


class GameController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.score_manager = ScoreManager()
        self.fruits = []
        self.bombs = []
        self.frames_since_last_fruit_spawn = 0
        self.frames_since_last_bomb_spawn = 0
        self.state = "menu"  # Stato iniziale: menu

        # Inizializza il menu e la schermata di sconfitta (inizialmente vuota)
        self.menu_screen = MenuScreen()
        self.loose_screen = None

        self.background = cv2.imread('C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/background.jpeg')

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
                self.score_manager.update_score(-50)

    def display_score(self, frame):
        font = cv2.FONT_HERSHEY_TRIPLEX
        score_text = f"Score: {self.score_manager.get_score()}"
        cv2.putText(frame, score_text, (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    def apply_background(self, frame):
        """Applica lo sfondo con opacità al frame della videocamera."""
        # Ridimensiona l'immagine di sfondo per adattarla al frame della videocamera
        background_resized = cv2.resize(self.background, (frame.shape[1], frame.shape[0]))

        # Imposta l'opacità
        opacity = 0.4
        cv2.addWeighted(background_resized, opacity, frame, 1 - opacity, 0, frame)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            hand_position = self.hand_tracker.track(frame)


            if self.state == "menu":
                # Visualizza menu e avvia il gioco se viene premuto 'Start'
                self.menu_screen.draw(frame)
                if hand_position and self.menu_screen.check_start(hand_position):
                    self.state = "playing"

            elif self.state == "playing":
                # Logica del gioco
                # Applica lo sfondo semi-trasparente al frame
                self.apply_background(frame)
                self.frames_since_last_fruit_spawn += 1
                if self.frames_since_last_fruit_spawn > 20:
                    self.spawn_fruit()
                    self.frames_since_last_fruit_spawn = 0

                self.frames_since_last_bomb_spawn += 1
                if self.frames_since_last_bomb_spawn > 40:
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

                # Controlla se il punteggio è sotto zero
                if self.score_manager.get_score() < 0:
                    self.loose_screen = LoseScreen(self.score_manager.get_score())
                    self.state = "game_over"

                self.display_score(frame)

            elif self.state == "game_over":
                # Visualizza schermata di sconfitta
                self.loose_screen.draw(frame)

            cv2.imshow("Fruit Ninja Game", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
