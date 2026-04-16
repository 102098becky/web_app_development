import sqlite3

DATABASE = 'instance/database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

class Ledger:
    def __init__(self, id, name, created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at

    @staticmethod
    def get_all():
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM ledgers ORDER BY created_at DESC').fetchall()
            return [Ledger(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(ledger_id):
        with get_db_connection() as conn:
            row = conn.execute('SELECT * FROM ledgers WHERE id = ?', (ledger_id,)).fetchone()
            if row:
                return Ledger(**dict(row))
            return None

    @staticmethod
    def create(name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ledgers (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def delete(ledger_id):
        with get_db_connection() as conn:
            conn.execute('DELETE FROM ledgers WHERE id = ?', (ledger_id,))
            conn.commit()
