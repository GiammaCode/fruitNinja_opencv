# game/loose_screen.py
import cv2

class LooseScreen:
    def __init__(self, final_score):
        self.final_score = final_score

    def draw(self, frame):
        """Visualizza il messaggio di sconfitta e il punteggio finale."""
        cv2.putText(frame, "GAME OVER", (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        score_text = f"Final Score: {self.final_score}"
        cv2.putText(frame, score_text, (150, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
