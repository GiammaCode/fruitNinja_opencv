import random
import cv2


class Fruit:
    """
    Represents a falling fruit object in the game. Each fruit has an image,
    an initial random position, a falling speed, and a status indicating if it's cut.

    Attributes:
        image (ndarray): The image of the fruit with transparency (alpha channel).
        x (int): Initial horizontal position of the fruit on the screen.
        y (int): Initial vertical position of the fruit (starting from the top).
        speed (int): Speed at which the fruit falls.
        is_cut (bool): Indicates whether the fruit has been sliced.
    """

    def __init__(self):
        """
        Initializes the Fruit object with a random position, speed, and loads the fruit image.
        """
        # local path
        # self.image = cv2.imread("../assets/images/apple.png",cv2.IMREAD_UNCHANGED)
        self.image = cv2.imread("C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/apple.png",
                                cv2.IMREAD_UNCHANGED)
        # define fruit position and speed
        self.x = random.randint(50, 600)
        self.y = 0
        self.speed = random.randint(5, 10)
        self.is_cut = False

    def update_position(self):
        """
        Updates the position of the fruit, making it fall by increasing its y-coordinate.
        Only updates if the fruit has not been cut.
        """
        if not self.is_cut:
            self.y += self.speed

    def check_collision(self, hand_position):
        """
       Checks if the fruit has collided with the user's hand position.

       Args:
           hand_position (tuple): The (x, y) position of the user's hand.

       Returns:
           bool: True if the hand is close enough to "slice" the fruit, otherwise False.
       """
        screen_width = 640
        screen_height = 480
        if hand_position:
            # to adact x,y of hand position with the video resolution
            hand_x, hand_y = int(hand_position.x * screen_width), int(hand_position.y * screen_height)
            # euclidea distance
            distance = ((hand_x - self.x) ** 2 + (hand_y - self.y) ** 2) ** 0.5
            return distance < 50  # min distance to have a collision

    def draw(self, frame):
        """
       Draws the fruit on the given frame with transparency.

       Args:
           frame (ndarray): The video frame where the fruit should be displayed.

       This method uses the alpha channel of the fruit image to overlay it
       on the frame, maintaining transparency.
       """
        h, w, _ = self.image.shape
        # check image shepe is correct (out of frame)
        if self.y + h >= frame.shape[0] or self.x + w >= frame.shape[1]:
            return

        # Normalize the alpha channel to apply transparency
        alpha_s = self.image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s  # background frame

        # Overlay the BGR channels of the fruit image onto the frame
        for c in range(3):  # bgr = 3
            frame[self.y:self.y + h, self.x:self.x + w, c] = (
                    alpha_s * self.image[:, :, c] +  # fruit pixel
                    alpha_l * frame[self.y:self.y + h, self.x:self.x + w, c]  # background pixel
            )
