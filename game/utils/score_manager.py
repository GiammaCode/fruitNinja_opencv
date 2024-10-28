class ScoreManager:
    """
    Manages the player's score in the game, allowing updates to the score
    and retrieval of the current score.

    Attributes:
        score (int): The current score of the player.
    """
    def __init__(self):
        """
        Initializes the ScoreManager with a starting score of zero.
        """
        self.score = 0

    def update_score(self, points):
        """
       Updates the player's score by adding the specified points.

       Args:
           points (int): The number of points to add to the current score.
       """
        self.score += points
        print(self.score)

    def get_score(self):
        """
       Retrieves the current score of the player.

       Returns:
           int: The current score.
       """
        return self.score
