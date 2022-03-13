class DatabaseGame:
    def __init__(
        self,
        player1,
        player2,
        board_size,
        player1_territory,
        player1_captures,
        player2_captures,
        player2_territory,
        time_allowed,
    ):
        self.player1 = player1
        self.player2 = player2
        self.board_size = board_size
        self.player1_territory = player1_territory
        self.player1_captures = player1_captures
        self.player2_captures = player2_captures
        self.player2_territory = player2_territory
        self.time_allowed = time_allowed
