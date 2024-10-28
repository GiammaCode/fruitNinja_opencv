import cv2
import time


class MenuScreen:
    """
   Represents the main menu screen with a pulsating "Start" button and a game title.
   The "Start" button can detect if the player's hand hovers over it to start the game.

   Attributes:
       button_position (tuple): The (x, y) position of the "Start" button.
       button_size (tuple): The width and height of the "Start" button.
       last_pulse_time (float): The last time the button pulsated, used to control the pulsating effect.
       pulse (bool): Indicates the current state of the pulsation effect (True for dimmed, False for bright).
   """
    def __init__(self):
        """
        Initializes the MenuScreen with default position and size for the "Start" button,
        and sets up the pulsating effect.
        """
        self.button_position = (250, 200)
        self.button_size = (150, 100)
        self.last_pulse_time = time.time()  # initialize time to pulse
        self.pulse = False

    def draw_rounded_rectangle(self, frame, top_left, bottom_right, color, radius=20, thickness=-1):
        """
      Draws a rounded rectangle for the "Start" button.

      Args:
          frame (ndarray): The video frame where the rounded rectangle is drawn.
          top_left (tuple): Coordinates of the top-left corner of the rectangle.
          bottom_right (tuple): Coordinates of the bottom-right corner of the rectangle.
          color (tuple): BGR color of the rectangle.
          radius (int): Radius for the rounded corners.
          thickness (int): Thickness of the rectangle edges. -1 for filled.
      """
        x1, y1 = top_left
        x2, y2 = bottom_right

        # Draw circles for rounded corners
        cv2.circle(frame, (x1 + radius, y1 + radius), radius, color, thickness)
        cv2.circle(frame, (x2 - radius, y1 + radius), radius, color, thickness)
        cv2.circle(frame, (x1 + radius, y2 - radius), radius, color, thickness)
        cv2.circle(frame, (x2 - radius, y2 - radius), radius, color, thickness)

        # draw rectangle
        cv2.rectangle(frame, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
        cv2.rectangle(frame, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

    def draw(self, frame):
        """
        Draws the game title and a pulsating "Start" button with a rounded rectangle.

        Args:
            frame (ndarray): The video frame where the title and button are drawn.
        """
        # game title
        font = cv2.FONT_HERSHEY_TRIPLEX
        title_text = f"FRUIT NINJA"
        cv2.putText(frame, title_text, (100, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

        # update button pulsing
        current_time = time.time()
        if current_time - self.last_pulse_time >= 0.5:
            self.pulse = not self.pulse
            self.last_pulse_time = current_time

        # change color for pulse
        button_color = (0, 200, 0) if self.pulse else (0, 255, 0)

        # draw the button
        x, y = self.button_position
        w, h = self.button_size
        self.draw_rounded_rectangle(frame, (x, y), (x + w, y + h), button_color, radius=20, thickness=-1)
        text_size, _ = cv2.getTextSize("START", font, 1, 2)
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(frame, "START", (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    def check_start(self, hand_position):
        """
        Checks if the player's hand is hovering over the "Start" button.

        Args:
            hand_position (tuple): The (x, y) position of the player's hand.

        Returns:
            bool: True if the hand is over the button, False otherwise.
        """
        x, y = self.button_position
        w, h = self.button_size
        if hand_position:
            hand_x, hand_y = int(hand_position.x * 640), int(hand_position.y * 480)
            return x <= hand_x <= x + w and y <= hand_y <= y + h
        return False
