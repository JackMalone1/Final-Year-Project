import sqlite3

conn = sqlite3.connect("zobrist.db")

c = conn.cursor()


def insert_zobrist_hash(zobrist_hash):
    with conn:
        c.execute(
            "INSERT INTO states VALUES (:id, :score)",
            {
                "id": str(zobrist_hash.id),
                "score": zobrist_hash.score,
            },
        )


def get_zobrist_by_hash(hash):
    c.execute(
        "SELECT * FROM states WHERE id=:hash",
        {"hash": str(hash)},
    )
    return c.fetchall()


def remove_zobrist_hash(zobrist_hash):
    with conn:
        c.execute(
            "DELETE from states WHERE id=:id AND score =: score",
            {"id": str(zobrist_hash.id), "score": zobrist_hash.score},
        )