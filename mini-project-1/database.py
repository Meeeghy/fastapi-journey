from contextlib import contextmanager
import sqlite3


class Database:

    def connect_to_db(self):
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                title TEXT,
                amount REAL,
                description TEXT
            )
        """)

    def get_all(self) -> list:
        self.cur.execute("SELECT * FROM transactions")
        rows = self.cur.fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get(self, id: int) -> dict | None:
        self.cur.execute("""
            SELECT * FROM transactions WHERE id = ?
        """, (id,))
        row = self.cur.fetchone()
        return self._row_to_dict(row) if row else None

    def create(self, item) -> int:
        self.cur.execute("SELECT MAX(id) FROM transactions")
        result = self.cur.fetchone()
        new_id = (result[0] or 0) + 1
        self.cur.execute("""
            INSERT INTO transactions
            VALUES (:id, :title, :amount, :description)
        """, {"id": new_id, "title": item.title, "amount": item.amount, "description": item.description})
        self.conn.commit()
        return new_id

    def update(self, id: int, item) -> dict | None:
        self.cur.execute("""
            UPDATE transactions
            SET title = :title, amount = :amount, description = :description
            WHERE id = :id
        """, {"id": id, "title": item.title, "amount": item.amount, "description": item.description})
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("""
            DELETE FROM transactions WHERE id = ?
        """, (id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

    def _row_to_dict(self, row) -> dict:
        return {
            "id": row[0],
            "title": row[1],
            "amount": row[2],
            "description": row[3]
        }


@contextmanager
def managed_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()