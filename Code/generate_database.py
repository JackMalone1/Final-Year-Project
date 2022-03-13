import sqlite3

conn = sqlite3.connect("go_data.db")

c = conn.cursor()

c.execute(
    """CREATE TABLE moves (
            colour text,
            player text,
            calculatedMoves integer,
            boardSize integer
            )"""
)

c.execute(
    """CREATE TABLE games (
            player1 text,
            player2 text,
            player1Territory integer,
            player1Captures integer,
            player2Territory integer,
            player2Captures integer,
            boardSize integer
            )"""
)
