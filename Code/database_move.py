class DatabaseMove:
    def __init__(
        self, colour, player, calculated_moves, board_size, time_allowed
    ):
        self.colour = colour
        self.player = player
        self.calculated_moves = calculated_moves
        self.board_size = board_size
        self.time_allowed = time_allowed
