import sqlite3

# conn = sqlite3.connect(':memory:')
conn = sqlite3.connect("zobrist.db")

c = conn.cursor()

c.execute(
    """CREATE TABLE states (
            id TEXT,
            score INTEGER
            )"""
)

conn.commit()
conn.close()
