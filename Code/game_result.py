class Result:
    """
    Stores the result of the game
    """
    def __init__(
        self,
        first_player,
        second_player,
        winner,
        score_difference,
    ):
        """
        Sets up all of the data to be stored
        :param first_player: string referencing who the first player was
        :param second_player: string referencing who the second player was
        :param winner: who won the game
        :param score_difference: how much the player won by
        """
        self.first_player = first_player
        self.second_player = second_player
        self.winner = winner
        self.score_difference = score_difference

    def __repr__(self):
        """
        Used for being able to print out the result
        :return: string representation of the class
        """
        return "Result('{}', '{}', '{}', {})".format(
            self.first_player,
            self.second_player,
            self.winner,
            self.score_difference,
        )
