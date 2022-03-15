import sqlite3

conn = sqlite3.connect("go_data.db")

c = conn.cursor()


def insert_move(move):
    with conn:
        c.execute(
            "INSERT INTO moves VALUES (:colour, :player, :calculatedMoves, :boardSize, :time_allowed, :move_number, :game_id)",
            {
                "colour": move.colour,
                "player": move.player,
                "calculatedMoves": move.calculated_moves,
                "boardSize": move.board_size,
                "time_allowed": move.time_allowed,
                "move_number": move.move_number,
                "game_id": move.game_id,
            },
        )


def get_moves_by_player(player):
    c.execute(
        "SELECT * FROM moves WHERE player=:player",
        {"last": player},
    )
    return c.fetchall()


def update_moves_calculated(move, moves_calculated):
    with conn:
        c.execute(
            """UPDATE moves SET calculatedMoves = :calculatedMoves
                    WHERE player=:player AND colour =: colour""",
            {
                "player": move.player,
                "colour": move.colour,
                "calculatedMoves": moves_calculated,
            },
        )


def remove_move(move):
    with conn:
        c.execute(
            "DELETE from moves WHERE player=:player AND colour =: colour",
            {"player": move.player, "colour": move.colour},
        )


def insert_game(game):
    with conn:
        c.execute(
            "INSERT INTO games VALUES (:player1, :player2, :player1Territory,"
            " :player1Captures, :player2Territory, :player2Captures, :boardSize, :time_allowed, :game_id)",
            {
                "player1": game.player1,
                "player2": game.player2,
                "player1Territory": game.player1_territory,
                "player1Captures": game.player1_captures,
                "player2Territory": game.player2_territory,
                "player2Captures": game.player2_captures,
                "boardSize": game.board_size,
                "time_allowed": game.time_allowed,
                "game_id": game.game_id,
            },
        )


def get_games_by_player_for_black(player):
    c.execute(
        "SELECT * FROM games WHERE player1=:player",
        {"player": player},
    )
    return c.fetchall()


def get_games_by_player_for_white(player):
    c.execute(
        "SELECT * FROM games WHERE player2=:player",
        {"player": player},
    )
    return c.fetchall()


def remove_game(game):
    with conn:
        c.execute(
            "DELETE from games WHERE player1=:player1 AND player2=:player2"
            " AND boardSize=:boardSize AND player1Territory=:player1Territory AND player1Captures=:player1Captures"
            " AND player2Territory=:player2Territory AND player2Captures=:player2Captures AND time_allowed=:time_allowed",
            {
                "player1": game.player1,
                "player2": game.player2,
                "boardSize": game.board_size,
                "player1Territory": game.player1_territory,
                "player1Captures": game.player1_captures,
                "player2Territory": game.player2_territory,
                "player2Captures": game.player2_captures,
                "time_allowed": game.time_allowed,
            },
        )
