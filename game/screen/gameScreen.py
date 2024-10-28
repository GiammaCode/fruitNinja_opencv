import cv2
from game.entities.bomb import Bomb
from game.entities.fruit import Fruit
from game.utils.hand_tracker import HandTracker
from game.screen.loseScreen import LoseScreen
from game.screen.menuScreen import MenuScreen
from game.utils.score_manager import ScoreManager


class GameController:
    """
   Controls the game logic, including handling the game states (menu, playing, game over),
   managing objects like fruits and bombs, tracking the player's hand, and displaying the score.

   Attributes:
       cap (cv2.VideoCapture): Captures video frames from the webcam.
       hand_tracker (HandTracker): Tracks the position of the player's hand.
       score_manager (ScoreManager): Manages and updates the player's score.
       fruits (list): List of active Fruit objects in the game.
       bombs (list): List of active Bomb objects in the game.
       frames_since_last_fruit_spawn (int): Counter to control the fruit spawning rate.
       frames_since_last_bomb_spawn (int): Counter to control the bomb spawning rate.
       state (str): Current state of the game ("menu", "playing", "game_over").
       menu_screen (MenuScreen): The main menu screen with a start button.
       loose_screen (LoseScreen): The game-over screen displayed when the game ends.
       background (ndarray): Background image to overlay onto the game frame.
   """
    def __init__(self):
        """
        Initializes the GameController with video capture, hand tracking, score manager,
        and the initial state set to "menu". Also sets up the background image.
        """
        self.cap = cv2.VideoCapture(0)
        self.hand_tracker = HandTracker()
        self.score_manager = ScoreManager()
        self.fruits = []
        self.bombs = []
        self.frames_since_last_fruit_spawn = 0
        self.frames_since_last_bomb_spawn = 0
        self.state = "menu"

        # Initialize the menu and game-over screens
        self.menu_screen = MenuScreen()
        self.loose_screen = None

        # Load the background image
        self.background = cv2.imread('../assets/images/background.jpeg')
        self.background = cv2.imread('C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/background.jpeg')

    def spawn_fruit(self):
        """
        Creates a new Fruit object and adds it to the list of active fruits.
        """
        fruit = Fruit()
        self.fruits.append(fruit)

    def spawn_bomb(self):
        """
       Creates a new Bomb object and adds it to the list of active bombs.
       """
        bomb = Bomb()
        self.bombs.append(bomb)

    def detect_cut_fruit(self, hand_position):
        """
      Checks for collisions between the player's hand and fruits, and updates
      the score if a fruit is sliced.

      Args:
          hand_position (tuple): Position of the player's hand in the frame.
      """
        for fruit in self.fruits:
            if not fruit.is_cut and fruit.check_collision(hand_position):
                fruit.is_cut = True
                self.score_manager.update_score(10)

    def detect_cut_bomb(self, hand_position):
        """
        Checks for collisions between the player's hand and bombs.
        Sets the game state to "game_over" if a bomb is sliced.

        Args:
            hand_position (tuple): Position of the player's hand in the frame.
        """
        for bomb in self.bombs:
            if not bomb.is_cut and bomb.check_collision(hand_position):
                bomb.is_cut = True
                self.state = "game_over"
                #self.score_manager.update_score(-50)

    def display_score(self, frame):
        """
        Displays the current score on the game frame.

        Args:
            frame (ndarray): The video frame to display the score on.
        """
        font = cv2.FONT_HERSHEY_TRIPLEX
        score_text = f"Score: {self.score_manager.get_score()}"
        cv2.putText(frame, score_text, (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    def apply_background(self, frame):
        """
        Applies a semi-transparent background overlay to the game frame.

        Args:
            frame (ndarray): The video frame to apply the background on.
        """
        # Resize background to match the frame dimensions
        background_resized = cv2.resize(self.background, (frame.shape[1], frame.shape[0]))

        # set opacity
        opacity = 0.4
        cv2.addWeighted(background_resized, opacity, frame, 1 - opacity, 0, frame)

    def run(self):
        """
       Main loop for running the game. Handles state transitions between menu, gameplay,
       and game-over screen, and displays each state accordingly.
       """
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            hand_position = self.hand_tracker.track(frame)

            # Manage different game states
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
                #if self.score_manager.get_score() < 0:
                #    self.loose_screen = LoseScreen(self.score_manager.get_score())
                #    self.state = "game_over"

                self.display_score(frame)

            elif self.state == "game_over":
                # Visualizza schermata di sconfitta
                self.loose_screen = LoseScreen(self.score_manager.get_score())
                self.loose_screen.draw(frame)

            cv2.imshow("Fruit Ninja Game", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
