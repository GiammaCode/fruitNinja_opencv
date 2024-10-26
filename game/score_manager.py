# game/score_manager.py
class ScoreManager:
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score
