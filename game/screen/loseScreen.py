import cv2
class LoseScreen:
    def __init__(self, final_score):
        self.final_score = final_score
        # Carica il classificatore per il rilevamento del volto
        self.face_cascade = cv2.CascadeClassifier('C:/Users/giamm/Desktop/fruitNinja_opencv/assets/classicator/haarcascade_frontalface_default.xml')

    def draw(self, frame):
        """Visualizza il messaggio di sconfitta 'Game Over' sulla fronte del giocatore."""
        # Disegna il punteggio finale sotto il messaggio "Game Over"
        font = cv2.FONT_HERSHEY_TRIPLEX
        score_text = f"Final Score: {self.final_score}"
        cv2.putText(frame, score_text, (150, 300), font, 1, (0, 0, 255), 2)

        # Converti il frame in scala di grigi per il rilevamento del volto
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Rileva i volti nel frame
        faces = self.face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Disegna "Game Over" sulla fronte del primo volto rilevato
        for (x, y, w, h) in faces:
            # Posiziona il testo sulla fronte
            text_position = (x + w // 6, y + h // 6)  # Sopra il volto

            # Disegna il testo "Game Over"
            cv2.putText(frame, "GAME OVER", text_position, font, 1, (0, 0, 255), 2, cv2.LINE_AA)

            # Disegna solo sulla fronte del primo volto rilevato e ignora gli altri
            break
