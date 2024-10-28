import random
import cv2


class Bomb:
    """
   Represents a falling bomb object in the game. Each bomb has an image,
   an initial random position, a falling speed, and a status indicating if it's been "sliced."

   Attributes:
       image (ndarray): The image of the bomb with transparency (alpha channel).
       x (int): Initial horizontal position of the bomb on the screen.
       y (int): Initial vertical position of the bomb (starting from the top).
       speed (int): Speed at which the bomb falls.
       is_cut (bool): Indicates whether the bomb has been sliced by the player.
   """

    def __init__(self):
        """
      Initializes the Bomb object with a random position, speed, and loads the bomb image.
      """
        # local path
        # self.image = cv2.imread("/assets/images/bomb.png", cv2.IMREAD_UNCHANGED)
        self.image = cv2.imread("C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/bomb.png",
                                cv2.IMREAD_UNCHANGED)
        self.x = random.randint(50, 600)
        self.y = 0
        self.speed = random.randint(5, 10)
        self.is_cut = False

    def update_position(self):
        """
        Updates the position of the bomb, making it fall by increasing its y-coordinate.
        Only updates if the bomb has not been sliced.
      """
        if not self.is_cut:
            self.y += self.speed

    def check_collision(self, hand_position):
        """
      Checks if the bomb has collided with the user's hand position.

      Args:
          hand_position (tuple): The (x, y) position of the user's hand.

      Returns:
          bool: True if the hand is close enough to "slice" the bomb, otherwise False.
      """
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            distance = ((hand_x - self.x) ** 2 + (hand_y - self.y) ** 2) ** 0.5
            return distance < 50

    def draw(self, frame):
        """
       Draws the bomb on the given frame with transparency.

       Args:
           frame (ndarray): The video frame where the bomb should be displayed.

       This method uses the alpha channel of the bomb image to overlay it
       on the frame, maintaining transparency.
       """
        h, w, _ = self.image.shape
        if self.y + h >= frame.shape[0] or self.x + w >= frame.shape[1]:
            return

        alpha_s = self.image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(3):
            frame[self.y:self.y + h, self.x:self.x + w, c] = (
                    alpha_s * self.image[:, :, c] +
                    alpha_l * frame[self.y:self.y + h, self.x:self.x + w, c]
            )
