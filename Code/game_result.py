class Result:
    def __init__(
        self,
        first_player,
        second_player,
        winner,
        score_difference,
    ):
        self.first_player = first_player
        self.second_player = second_player
        self.winner = winner
        self.score_difference = score_difference

    def __repr__(self):
        return "Result('{}', '{}', '{}', {})".format(
            self.first_player,
            self.second_player,
            self.winner,
            self.score_difference,
        )
