class DatabaseMove:
    def __init__(
        self,
        colour,
        player,
        calculated_moves,
        board_size,
        time_allowed,
        move_number,
        game_id,
    ):
        self.colour = colour
        self.player = player
        self.calculated_moves = calculated_moves
        self.board_size = board_size
        self.time_allowed = time_allowed
        self.move_number = move_number
        self.game_id = game_id
