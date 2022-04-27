"""
This script is used for basic database crud for the main database in the game.
There are functions for adding game results as well as specific moves that were done in each game
which will be automatically added to the database.
Use sqlite3 as well as a database on disk for storage of the results.
Also allows the user to remove moves and games based on players or full games respectively
You can also get moves for a specific player, update moves and get games for a specific player where they
were playing black or white
"""


import sqlite3

conn = sqlite3.connect("go_data.db")

c = conn.cursor()


def insert_move(move):
    """
    Adds the move passed in in to the database table.
    :param move: Move that you want to be added in to the database
    """
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
    """
    Gets all moves by the player that was passed in. This player will be either a string representing the monte carlo tree
    search or the alpha beta tree search. If there are moves that are related to an actual player then you can also get
    these values
    :param player: player that you want to get the moves for
    :return: all moves that are related to this player
    """
    c.execute(
        "SELECT * FROM moves WHERE player=:player",
        {"last": player},
    )
    return c.fetchall()


def update_moves_calculated(move, moves_calculated):
    """
    takes in a move that you want to udpate along with the number of moves calculated that you want to overwrite the old value
    with
    :param move: move that you want to update
    :param moves_calculated: new moves calculated value that you want
    """
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
    """
    Removes any moves from the database that matches the move that was passed in
    :param move: Move that you want to be removed from the database
    """
    with conn:
        c.execute(
            "DELETE from moves WHERE player=:player AND colour =: colour",
            {"player": move.player, "colour": move.colour},
        )


def insert_game(game):
    """
    Inserts the game passed in to the database
    :param game: game that you want to be added to the database
    """
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
    """
    Gets all games made by the player passed in for games where they were playing as black
    :param player: string representing the player that you want to get the moves for
    :return: list of all moves that match the player for black
    """
    c.execute(
        "SELECT * FROM games WHERE player1=:player",
        {"player": player},
    )
    return c.fetchall()


def get_games_by_player_for_white(player):
    """
    Gets all games made by the player passed in for games where they were playing as white
    :param player: string representing the player that you want to get the moves for
    :return: list of all moves that match the player for white
    """
    c.execute(
        "SELECT * FROM games WHERE player2=:player",
        {"player": player},
    )
    return c.fetchall()


def remove_game(game):
    """
    Removes all games that match the move that was passed in to the function. The ids do not necessarily need to match for the
    game to be deleted
    :param game: Game that you want to delete from the database
    """
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
