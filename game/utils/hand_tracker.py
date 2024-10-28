import cv2
import mediapipe as mp

class HandTracker:
    """
    Tracks the position of the user's hand in real-time using MediaPipe.
    Specifically, it identifies the position of the index finger tip to enable interaction.

    Attributes:
        mp_hands (mediapipe.python.solutions.hands): MediaPipe Hands module for hand detection.
        hands (mediapipe.python.solutions.hands.Hands): Instance of the Hands model with specific confidence thresholds.
        mp_drawing (mediapipe.python.solutions.drawing_utils): Utility for drawing hand landmarks on frames.
    """
    def __init__(self):
        """
       Initializes the HandTracker with MediaPipe's Hands solution and sets confidence levels
       for detection and tracking.
       """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

    def track(self, frame):
        """
       Detects the hand in the given video frame and identifies the position of the index finger tip.
       Draws hand landmarks on the frame if a hand is detected.

       Args:
           frame (ndarray): The BGR video frame from the webcam.

       Returns:
           hand_position (mediapipe.python.framework.landmark_pb2.NormalizedLandmark or None):
               Coordinates of the index finger tip (landmark 8) in normalized values (0 to 1),
               or None if no hand is detected.
       """
        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        # Process the RGB frame to detect hands
        results = self.hands.process(rgb_frame)
        hand_position = None

        # Check if any hands were detected and extract index finger tip position
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the original frame
                self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Set hand_position to the tip of the index finger (landmark 8)
                hand_position = hand_landmarks.landmark[8]
                break

        return hand_position
