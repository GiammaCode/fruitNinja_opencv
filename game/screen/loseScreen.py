import cv2
class LoseScreen:
    """
   Represents the game-over screen shown when the player's score drops below zero.
   Displays a "Game Over" message on the player's forehead and shows the final score.

   Attributes:
       final_score (int): The final score of the player at the end of the game.
       face_cascade (cv2.CascadeClassifier): Haar Cascade classifier used for face detection.
   """
    def __init__(self, final_score):
        """
       Initializes the LoseScreen with the player's final score and loads the face detection model.

       Args:
           final_score (int): The score to display when the game ends.
       """
        self.final_score = final_score
        # load classifier
        #self.face_cascade = cv2.CascadeClassifier('../assets/classicator/haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier('C:/Users/giamm/Desktop/fruitNinja_opencv/assets/classicator/haarcascade_frontalface_default.xml')

    def draw(self, frame):
        """
        Displays the "Game Over" message and final score on the frame.
        If a face is detected, places "Game Over" on the player's forehead.

        Args:
            frame (ndarray): The video frame where the "Game Over" message and score should be displayed.
        """
        font = cv2.FONT_HERSHEY_TRIPLEX
        score_text = f"Final Score: {self.final_score}"
        cv2.putText(frame, score_text, (150, 300), font, 1, (0, 0, 255), 2)

        # Convert the frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Display "Game Over" on the forehead of the first detected face
        for (x, y, w, h) in faces:
            # Position the "Game Over" text slightly above the detected face
            text_position = (x + w // 6, y + h // 6)  # Sopra il volto
            cv2.putText(frame, "GAME OVER", text_position, font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            break
